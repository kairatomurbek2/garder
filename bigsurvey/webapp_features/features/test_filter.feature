@test
@test_filter
Feature: Tests Filtration

  @keep_db
  Scenario: TestsFiltration
    Given I logged in as "root"
    And I open "test_list" page
    When I fill in following fields with following values
      | field          | value       |
      | customer       | QAZ2WSX     |
      | city           | Washington  |
      | address        | White House |
      | test_date_from | 2015-01-27  |
      | test_date_to   | 2015-01-27  |
    And I select "DOC121" from "pws"
    And I select "irrigation" from "service_type"
    And I select "Digester" from "hazard_type"
    And I select "PVB" from "bp_type"
    And I select "tester" from "tester"
    And I select "Failed" from "test_result"
    And I submit "test_filter" form
    Then I should see following
      | text          |
      | QAZ2WSX       |
      | Jan. 27, 2015 |
    And I should not see following
      | text    |
      | Seattle |
      | VALVE   |