#Background
@given('a database of perovskite properties and crystal structures')
def get_metal_oxide_data():
    structure = deftpy.get_data("MP-API-KEY") 
    return structure

#Scenario 1
@given('a specific perovskite structure is selected by the user')
def get_descriptors(structure):
    descriptors = deftpy.get_descriptor_data(structure)
    return descriptors # 2x1 array in format of [Eb, Vr]

@when('the user inputs this structure into the defect energy prediction tool')
def predict_defect_energy(structure, descriptors):
    predicted_energy = deftpy.predict_energy(structure, descriptors)
    return predicted_energy

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