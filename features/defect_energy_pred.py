#Background
@given('a database of metal oxide properties and defect formation energies')
def get_metal_oxide_data():
    return deft_py.get_data("METAL_OXIDE_DB_LINK")  # either database link or MP API key

#Scenario 1
@given('a specific metal oxide composition is selected by the user')
def get_composition(composition):
    return deft_py.get_composition_data(composition)

@when('the user inputs this composition into the defect energy prediction tool')
def predict_defect_energy(composition):
    predicted_energy = deft_py.predict_energy(composition)
    return predicted_energy

@then('display the predicted defect formation energy')
def display_predicted_energy(predicted_energy):
    print(f"Predicted Defect Formation Energy for {composition}: {predicted_energy} eV")

#Scenario 2
@given('multiple metal oxide compositions are selected by the user')
def get_multiple_compositions(*compositions):
    return [deft_py.get_composition_data(comp) for comp in compositions]

@when('the system calculates the defect formation energies for these compositions')
def calculate_energies(compositions):
    energies = [deft_py.predict_energy(comp) for comp in compositions]
    return energies

@then('display a comparative analysis of defect formation energies')
def display_comparative_analysis(compositions, energies):
    plt.bar(compositions, energies)
    plt.xlabel('Metal Oxide Composition')
    plt.ylabel('Defect Formation Energy (eV)')
    plt.title('Comparative Analysis of Defect Formation Energies')
    plt.show()
  
