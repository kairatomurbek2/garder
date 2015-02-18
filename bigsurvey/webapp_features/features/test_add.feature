@test_add
Feature: Test adding


  Scenario Outline: Test adding page access
    Given I logged in as "<role>"
    When I directly open "test_add" page for hazard with pk "<pk>"
    Then I should <reaction> "Not Found"
    And I logout
  Examples:
    | role     | pk | reaction |
    | root     | 1  | not see  |
    | root     | 2  | not see  |
    | admin    | 1  | not see  |
    | admin    | 2  | see      |
    | surveyor | 1  | see      |
    | surveyor | 2  | see      |
    | tester   | 1  | not see  |
    | tester   | 2  | see      |


  Scenario: Correct test adding
    Given I logged in as "root"
    And I open "test_add" page for hazard with pk "1"
    And I fill in following fields with following values
      | field                 | value      |
      | test_serial_number    | TSN123321  |
      | last_calibration_date | 2015-02-15 |
      | cv1_gauge_pressure    | 123456     |
    And I select "Wilkins" from "test_manufacturer"
    And I select "tester" from "tester"
    When I submit "test" form
    Then I should be at "hazard_detail" page with pk "1"
    And I should see "test adding success" message
    And I should see following
      | text          |
      | TSN123321     |
      | Feb. 15, 2015 |
      | Wilkins       |
      | 123456        |


  Scenario: Incorrect test adding
    Given I logged in as "root"
    And I open "test_add" page for hazard with pk "1"
    And I fill in "last_calibration_date" with "not a valid date"
    When I submit "test" form
    Then I should be at "test_add" page for hazard with pk "1"
    And I should see "test adding error" message
    And I should see following validation error messages on following fields
      | field                 | error_message           |
      | test_serial_number    | This field is required. |
      | last_calibration_date | Enter a valid date.     |
      | test_manufacturer     | This field is required. |