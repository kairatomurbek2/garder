@letter
@letter_filter
Feature: Hazard Filtration

  @keep_db
  Scenario: HazardFiltration
    Given I logged in as "root"
    And I open "hazard_list" page
    When I fill in following fields with following values
      | field              | value       |
      | customer           | QAZ2WSX     |
      | city               | Washington  |
      | address            | White House |
      | due_test_date_from | 2015-05-31  |
      | due_test_date_to   | 2015-05-31  |
    And I select "DOC121" from "pws"
    And I select "irrigation" from "service_type"
    And I select "Digester" from "hazard_type"
    And I select "Due Install" from "assembly_status"
    And I select "PVB" from "bp_type_present"
    And I select "PVB" from "bp_type_required"
    And I submit "hazard_filter" form
    Then I should see following
      | text         |
      | QAZ2WSX      |
      | May 31, 2015 |
    And I should not see following
      | text    |
      | Seattle |
      | VALVE   |