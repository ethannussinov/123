


#Background
@given('an API key is provided and a the user has perovskite identifiers')
# This function will use the perovskite name(s) to access the POSCAR structure via API connection. 
# It will then use this to construct an instance of class Crystal, which will be serialized and stored.
def get_perovskite_structure(*perovskites, API):
    structures = {}
    for perovskite in perovskites:
        structure = deftpy.get_data(perovskite, API)
        structures[perovskite] = structure
    return structures

#Scenario 1
@given('a single perovskite structure is selected by the user')
# This function will recieve the serialized Crystal instance, which it will process
# It will then index the Eb and Vr datasets for their respective values, which will be 
# stored as attributes of the class.
def get_descriptors(structure):
    bond_diss_enthalpy = deftpy.get_eb(structure)
    reduction_potential = deftpy.get_vr(structure)
    return (structure, bond_diss_enthalpy, reduction_potential)

@when('the user inputs this structure into the defect energy prediction tool')
# This function will use the Crystal instance and descriptors to predict the defect energy. 
def predict_defect_energy(structure, descriptors):
    predicted_energy = deftpy.predict_energy(structure, descriptors)
    return (structure, predicted_energy)

@then('display the predicted defect formation energy')
def display_predicted_energy(structure, predicted_energy):
    print(f"Predicted Defect Formation Energy for {structure}: {predicted_energy} eV")

#Scenario 2
@given('multiple perovskite structures are selected by the user')
def get_multiple_compositions(*structures):
    descriptors = [deftpy.get_descriptor_data(struc) for struc in structures]
    return descriptors

@when('the system calculates the defect formation energies for these structures')
def calculate_energies(structures, descriptors):
    energies = [deftpy.predict_energy(struc) for struc in structures]
    return energies

@then('display a comparative analysis of defect formation energies')
def display_comparative_analysis(structures, energies):
    plt.bar(structures, energies)
    plt.xlabel('Perovskite Structure')
    plt.ylabel('Defect Formation Energy (eV)')
    plt.title('Comparative Analysis of Defect Formation Energies')
    plt.show()