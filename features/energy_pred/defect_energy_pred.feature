Feature: defect_energy_pred
 	This feature aims to predict the formation energy of defects in perovskites 
  based on their composition and structure. 

 Background:
    Given a database of perovskite properties and crystal structures

  Scenario: Predicting defect formation energy for a single structure
    Given a specific perovskite structure is selected by the user
    When the user inputs this structure into the defect energy prediction tool
    Then display the predicted defect formation energy

  Scenario: Comparing defect formation energies for multiple structures
    Given multiple perovskite structures are selected by the user
    When the system calculates the defect formation energies for these structures
    Then display a comparative analysis of defect formation energies