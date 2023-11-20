import re
import sys
from enum import Enum
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Callable

import numpy as np
import pandas as pd
import sqlalchemy as sa
import pickle

from pymatgen.ext.matproj import MPRester
from pymatgen.analysis.defects.generators import VacancyGenerator
from pymatgen.analysis.local_env import CrystalNN
from pymatgen.core import Species, Structure

EB_DICT = {"filepath": "../../data/Eb.csv", "column_name": "Eb", "comparison": "os"}
VR_DICT = {"filepath": "../../data/Vr.csv", "column_name": "Vr", "comparison": "n"}


class Crystal:

    @staticmethod
    def _split_before_first_number(s: str) -> List[str]:

        return re.split(r"(?=\d)", s, maxsplit=1)

    @staticmethod
    def _parse_species_string(species_string: str) -> Tuple[Optional[Species], str, int]:

        # Check if the string is of valid format before trying to parse
        if not re.match(r"[A-Za-z]+\d+\+", species_string):
            split_str = Crystal._split_before_first_number(species_string)
            return None, split_str[0], round(float(split_str[1][:-1]))

        species = Species.from_string(species_string)
        return species, species.symbol, species.oxi_state

    def __init__(
            self,
            filepath: Optional[str] = None,
            poscar_string: Optional[str] = None,
            pymatgen_structure: Optional[Structure] = None,
            nn_finder: Optional[CrystalNN] = None,
            use_weights: Optional[bool] = False,
            species_symbol: Optional[str] = "O"
    ):

        if filepath:
            self.structure = Structure.from_file(filepath)
        elif poscar_string:
            self.structure = Structure.from_str(poscar_string, fmt="poscar")
        elif pymatgen_structure:
            self.structure = pymatgen_structure
        else:
            raise ValueError("Specify either filepath, poscar_string, or pymatgen_structure.")

        self.nn_finder = nn_finder or CrystalNN()
        self.use_weights = use_weights

        self.species_symbol = species_symbol

        package_dir = Path(__file__).parent
        self.eb = pd.read_csv(package_dir / EB_DICT["filepath"])
        self.vr = pd.read_csv(package_dir / VR_DICT["filepath"])

        self._cn_dicts_initialized = False
        self.cn_dicts = []
        self.bond_dissociation_enthalpies = self._get_values(self.eb, EB_DICT["column_name"], EB_DICT["comparison"])
        self.reduction_potentials = self._get_values(self.vr, VR_DICT["column_name"], VR_DICT["comparison"])

    def _initialize_structure_analysis(self) -> List[Dict[str, int]]:

        if self._cn_dicts_initialized:
            return self.cn_dicts

        # Check for oxidation states and add them if they are not present in the structure object already
        if sum([x.oxi_state != 0 for x in self.structure.species]) == 0:
            self.structure.add_oxidation_state_by_guess()
        vacancy_generator = VacancyGenerator()
        vacancies = vacancy_generator.get_defects(self.structure)
        indices = [v.defect_site_index for v in vacancies if v.site.specie.symbol == self.species_symbol]
        self.cn_dicts = [self.nn_finder.get_cn_dict(self.structure, i, use_weights=self.use_weights) for i in indices]
        self._cn_dicts_initialized = True
        return self.cn_dicts

    def _get_values(self, dataframe: pd.DataFrame, column_name: str, comparison: str) -> List[Dict[str, float]]:

        self._initialize_structure_analysis()
        values = []
        for cn_dict in self.cn_dicts:
            value = {}
            for species_string, cn in cn_dict.items():
                species = Species.from_string(species_string)
                symbol = species.symbol
                oxidation_state = species.oxi_state
                condition = (dataframe.elem == symbol) & (dataframe[comparison] == oxidation_state)
                if not dataframe.loc[condition, column_name].empty:
                    value[species_string] = dataframe.loc[condition, column_name].iloc[0]
                else:
                    value[species_string] = np.nan
            values.append(value)
        return values

    def to_pickle(self):

        return pickle.dumps(self)

    @staticmethod
    def from_pickle(pickle_data):

        return pickle.loads(pickle_data)
    

def get_perovskite_structure(perovskite, API):

    with MPRester(API) as mpr:
        # Query for structures and band gap energies
        results = mpr.query(criteria={"pretty_formula": perovskite},
                            properties=["cif", "band_gap"])

        if results:
            # Assume the first result is the desired one
            structure_cif = results[0]["cif"]
            band_gap_energy = results[0]["band_gap"]
            
            # Optionally write the POSCAR file content to a file
            with open(f"{perovskite}_POSCAR", "w") as file:
                file.write(structure_cif)
            
            print(f"Band gap energy for {perovskite}: {band_gap_energy} eV")

            crystal = Crystal(poscar_string=structure_cif)
            
            crystal.eg = band_gap_energy

            crystal_pickle = crystal.to_pickle()

            return crystal_pickle, band_gap_energy
        else:
            print(f"No results found for {perovskite}")
            return None, None
        

def get_descriptors(structure):
    crystal = structure.from_pickle()

    CN = crystal.cn_dicts
    Eb = crystal.bond_dissociation_enthalpies
    Vr = crystal.reduction_potentials

# Calculate CN-weighted Eb sum
    Eb_sum = []
    for CN_dict, Eb_dict in zip(CN, Eb):
        CN_array = np.array(list(CN_dict.values()))
        Eb_array = np.array(list(Eb_dict.values()))
        Eb_sum.append(np.sum(CN_array * Eb_array))

    # Calculate maximum Vr
    Vr_max = []
    for Vr_dict in Vr:
        try:
            Vr_max.append(max(Vr_dict.values()))
        except ValueError:
            Vr_max.append(np.nan)

    # Make a dataframe
    df_ 
    formula = df_defectid["formula"].values
    defectid = df_defectid["defectid"].values
    site = df_defectid["site"].values
    Eg = df_defectid["bandgap_eV"].values
    Ev = df_defectid["dH_eV"].values
    try:
        df_cf = pd.concat(
            [
                df_cf,
                pd.DataFrame(
                    {
                        "formula": formula,
                        "defectid": defectid,
                        "site": site,
                        "Eb_sum": Eb_sum,
                        "Vr_max": Vr_max,
                        "Eg": Eg,
                        "Ev": Ev,
                    }
                ),
            ]
        )
    except ValueError:
        pass
df_cf = df_cf.reset_index(drop=True)



    return (structure, Eb, Vr)


def compute_properties(serialized_crystals):
    # Logic to unserialize, compute additional properties, and re-serialize
    pass

def apply_predictive_model(serialized_crystals):
    # Logic to unserialize, apply predictive model, and re-serialize
    pass

def insert_into_db(dataframe, table_name):
    # Logic to insert data into DuckDB
    pass

def main():
    # Step 1: Initialization
    initial_data = initialize_crystals(perovskites, API)
    initial_df = pd.DataFrame(initial_data)
    insert_into_db(initial_df, 'raw_perovskite_data')

    # Step 2: Analysis
    analyzed_data = compute_properties(initial_df['serialized_crystal'])
    analyzed_df = pd.DataFrame(analyzed_data)
    insert_into_db(analyzed_df, 'ind_perovskite_data')

    # Step 3: Prediction
    predicted_data = apply_predictive_model(analyzed_df['serialized_crystal'])
    predicted_df = pd.DataFrame(predicted_data)
    insert_into_db(predicted_df, 'energy_pred_model')

if __name__ == "__main__":
    main()