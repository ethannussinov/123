Feature: defect_energy_pred
 	This feature aims to predict the formation energy of defects in metal oxides based on their composition and structure. 

Background:
 	Given we have a database of metal oxide properties and defect formation energies.
		
  Scenario: Predict defect energy for a given composition
      Given a user has selected a specific metal oxide composition,
      When they input this composition into the defect energy prediction tool,
      Then the system calculates and displays the predicted defect formation energy.
		

  Scenario: Compare defect energy across different metal oxides
      Given the user is interested in comparing different metal oxides,
       When they select multiple metal oxide compositions,
       Then the system calculates and displays a comparative analysis of defect formation energies for these compositions.
