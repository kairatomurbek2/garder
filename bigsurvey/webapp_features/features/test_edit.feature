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
    | admin    | 2  | not see  |
    | admin    | 1  | see      |
    | surveyor | 1  | see      |
    | surveyor | 2  | see      |
    | tester   | 2  | not see  |
    | tester   | 1  | see      |


  Scenario: Correct test editing
    Given I logged in as "root"
    And I open "test_edit" page with pk "2"
    And I fill in following fields with following values
      | field              | value  |
      | cv2_gauge_pressure | 111111 |
    When I submit "test" form
    Then I should be at "hazard_detail" page with pk "2"
    And I should see "test editing success" message
    And I should see "111111"