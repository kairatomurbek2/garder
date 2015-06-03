@test_add
Feature: Test adding


  Scenario Outline: Test adding page access
    Given I logged in as "<role>"
    When I directly open "test_add" page for hazard with pk "<pk>"
    Then I should <reaction> "Page not found"
    And I logout
  Examples:
    | role     | pk | reaction |
    | root     | 1  | not see  |
    | root     | 2  | not see  |
    | admin    | 2  | not see  |
    | admin    | 1  | see      |
    | surveyor | 1  | see      |
    | surveyor | 2  | see      |
    | tester   | 2  | not see  |
    | tester   | 1  | not see  |


  Scenario: Correct test adding
    Given I logged in as "tester"
    And I open "test_add" page for hazard with pk "2"
    And I fill in following fields with following values
      | field              | value  |
      | cv1_gauge_pressure | 123456 |
      | air_inlet_psi      | 16     |
    And I select "tester" from "tester"
    And I choose "True" from "test_result"
    And I check "rv_did_not_open"
    And I check "cv_leaked"
    When I submit "test" form
    Then I should be at "hazard_detail" page with pk "2"
    And I should see "test adding success" message
    When I logout
    And I login as "tester"
    And I open "unpaid_test_list" page
    Then I should see following
      | text   |
      | tester |
      | Passed |
      | VALVE  |