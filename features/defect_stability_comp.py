#Background
@given('data on defect formation energies and environmental conditions for metal oxides')
def get_defect_stability_data():
    return deft_py.get_stability_data("STABILITY_DB_LINK")  # either database link or MP API key

#Scenario 1
@given('a specific defect in a metal oxide is selected by the user')
def get_defect_data(defect):
    return deft_py.get_defect_data(defect)

@when('the user inputs different environmental conditions')
def analyze_stability(defect, conditions):
    stability_data = deft_py.calculate_stability(defect, conditions)
    return stability_data

@then('display the stability of the defect under these conditions')
def display_stability_map(stability_data):
    # Assuming stability_data is a dict with conditions as keys and stability as values
    plt.plot(stability_data.keys(), stability_data.values())
    plt.xlabel('Conditions')
    plt.ylabel('Defect Stability')
    plt.title('Defect Stability under Varying Conditions')
    plt.show()

#Scenario 2
@given('multiple metal oxides are selected by the user for a specific environmental condition')
def get_multiple_oxides(*oxides):
    return [deft_py.get_oxide_data(oxide) for oxide in oxides]

@when('the system calculates the stability of defects under the given condition')
def calculate_stabilities(oxides, condition):
    stabilities = [deft_py.calculate_stability(oxide, condition) for oxide in oxides]
    return stabilities

@then('display a comparative analysis of defect stabilities')
def display_comparative_stability(oxides, stabilities):
    plt.bar(oxides, stabilities)
    plt.xlabel('Metal Oxide')
    plt.ylabel('Defect Stability')
    plt.title(f'Comparative Analysis of Defect Stabilities under {condition}')
    plt.show()


