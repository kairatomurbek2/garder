@test_edit
Feature: Test editing


  Scenario Outline: Test editing page access
    Given I logged in as "<role>"
    When I directly open "test_edit" page with pk "<pk>"
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


  Scenario: Correct test editing
    Given I logged in as "root"
    And I open "test_edit" page with pk "1"
    And I fill in following fields with following values
      | field              | value  |
      | cv2_gauge_pressure | 111111 |
    When I submit "test" form
    Then I should be at "hazard_detail" page with pk "1"
    And I should see "test editing success" message
    And I should see "111111"


  Scenario: Incorrect test editing
    Given I logged in as "root"
    And I open "test_edit" page with pk "1"
    And I fill in following fields with following values
      | field                 | value            |
      | test_serial_number    |                  |
      | last_calibration_date | not a valid date |
    When I submit "test" form
    Then I should be at "test_edit" page with pk "1"
    And I should see "test editing error" message
    And I should see following validation error messages on following fields
      | field                 | error_message           |
      | last_calibration_date | Enter a valid date.     |
      | test_serial_number    | This field is required. |