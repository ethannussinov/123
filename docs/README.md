# Crystal Class Documentation

## Overview
The `Crystal` class provides functionality for analyzing crystal structures, specifically focused on perovskite materials. It utilizes the pymatgen library to work with crystallographic structures and calculate various physical and chemical properties.

## Attributes
- `structure`: A pymatgen `Structure` object representing the crystal structure.
- `nn_finder`: An instance of `CrystalNN` used to find the nearest neighbors in the structure.
- `eg`: The band gap energy of the crystal.
- `eb`: A DataFrame containing bond dissociation enthalpies.
- `vr`: A DataFrame containing reduction potentials.
- `cn_dicts`: A list of dictionaries with coordination numbers for each site.
- `bond_dissociation_enthalpies`: A list of bond dissociation enthalpies calculated for the crystal.
- `reduction_potentials`: A list of reduction potentials calculated for the crystal.

## Methods

### `to_pickle`
Serializes the `Crystal` object to a binary format using the `pickle` module.

**Returns:**
- A bytes object representing the serialized `Crystal` instance.

### `from_pickle`
Deserializes a `Crystal` object from a binary format.

**Arguments:**
- `pickle_data` (bytes): The binary data to deserialize.

**Returns:**
- A `Crystal` instance reconstructed from the binary data.

## Usage Examples
(Include a few examples of how to use the `Crystal` class, initialize it, serialize, deserialize, and visualize the structure.)

## Installation
(Include instructions on how to set up the environment to use the `Crystal` class, including installing pymatgen and any other dependencies.)

## Contributing
(If this is a collaborative project, provide guidelines on how others can contribute to the development of the `Crystal` class.)

## License
(Include information about the license under which the `Crystal` class is released.)



import re
import sys
from enum import Enum
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Callable

import numpy as np
import pandas as pd
import sqlalchemy as sa
import pickle

from pymatgen.analysis.defects.generators import VacancyGenerator
from pymatgen.analysis.local_env import CrystalNN
from pymatgen.core import Species, Structure

EB_DICT = {"filepath": "../../data/Eb.csv", "column_name": "Eb", "comparison": "os"}
VR_DICT = {"filepath": "../../data/Vr.csv", "column_name": "Vr", "comparison": "n"}


class Crystal:
    """
    A class for analyzing crystal structures.

    Attributes:
        structure: The pymatgen Structure object.
        nn_finder: The CrystalNN object.
        eg: The band gap energy.
        eb: The bond dissociation enthalpies.
        vr: The reduction potentials.
        cn_dicts: A list of coordination number dictionaries.
        bond_dissociation_enthalpies: A list of bond dissociation enthalpies.
        reduction_potentials: A list of reduction potentials.


    Methods:
       to_pickle: Serializes the Crystal object to a binary format using the `pickle` module.
       from_pickle: Deserializes a Crystal object from a binary format.
    """

    @staticmethod
    def _split_before_first_number(s: str) -> List[str]:
        """
        Splits a string before the first number.

        Args:
            s: The string to split.

        Returns:
            A list of strings.
        """
        return re.split(r"(?=\d)", s, maxsplit=1)

    @staticmethod
    def _parse_species_string(species_string: str) -> Tuple[Optional[Species], str, int]:
        """
        Parses a species string.

        Args:
            species_string: The species string to parse.

        Returns:
            A tuple of the species, the symbol, and the oxidation state.
        """
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
        """
        Initializes the Crystal object.

        Args:
            filepath: The filepath to the POSCAR file.
            poscar_string: The POSCAR string.
            pymatgen_structure: The pymatgen Structure object.
            nn_finder: The CrystalNN object.

        Raises:
            ValueError: If neither filepath, poscar_string, nor pymatgen_structure is specified.
        """
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
        """
        Initializes the structure analysis.

        Returns:
            A list of coordination number dictionaries.
        """
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
        """
        Gets the values from the dataframe.

        Args:
            dataframe: The dataframe.
            column_name: The column name.
            comparison: The comparison column name.

        Returns:
            A list of dictionaries.
        """
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
        """
        Serializes the Crystal object to a binary format using the `pickle` module.

        This method is useful for converting the Crystal instance into a format 
        that can be saved to a file or a database as a binary blob.

        Returns:
            A bytes object representing the serialized Crystal instance.
        """
        return pickle.dumps(self)

    @staticmethod
    def from_pickle(pickle_data):
        """
        Deserializes a Crystal object from a binary format.

        This static method reconstructs a Crystal instance from its serialized
        binary representation, which can be useful when loading a Crystal object
        from a file or a database where it has been stored as a binary blob.

        Args:
            pickle_data (bytes): The binary data to deserialize.

        Returns:
            A Crystal instance reconstructed from the binary data.
        """
        return pickle.loads(pickle_data)



            """
    Retrieves the POSCAR file content and band gap energy for a given material formula
    from the Materials Project database.

    Args:
        material_formula (str): The formula of the material, e.g., 'CaTiO3'.
        api_key (str): Your Materials Project API key.

    Returns:
        tuple: A tuple containing the POSCAR file content as a string and the band gap energy as a float.
    """