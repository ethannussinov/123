Feature: defect_stability_comp
This feature aims to analyze and compare the stability of defects in various metal oxides under different environmental conditions.

Background: 
Given we have data on defect formation energies and environmental conditions (like temperature and pressure) for different metal oxides.
			
Scenario: Stability analysis of a specific defect in varying conditions
     Given a user selects a specific defect in a metal oxide,
When they input different environmental conditions (e.g., varying temperatures and pressures),
     Then the system calculates and displays the stability of the defect under these conditions, perhaps in the form of a stability map or graph.

Scenario: Comparative analysis of defect stabilities in metal oxides.
      Given the user wants to compare the stability of a specific type of defect across different metal oxides,
      When they select multiple metal oxides and specify an environmental condition,
      Then the system calculates and displays a comparative analysis, showing how the stability of the defect varies across these oxides under the given condition.

