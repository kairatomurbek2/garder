@inspection_edit
Feature: Inspection editing


  Scenario Outline: Inspection editing page access
    Given I logged in as "<role>"
    When I directly open "inspection_edit" page with pk "<pk>"
    Then I should <reaction> "Not Found"
    And I logout
  Examples:
    | role     | pk | reaction |
    | root     | 1  | not see  |
    | root     | 2  | not see  |
    | admin    | 1  | see      |
    | admin    | 2  | not see  |
    | surveyor | 1  | see      |
    | surveyor | 2  | see      |
    | tester   | 1  | see      |
    | tester   | 2  | see      |


  Scenario: Correct Inspection editing
    Given I logged in as "root"
    And I open "inspection_edit" page with pk "1"
    And I fill in "notes" with "This is test notes"
    When I submit "inspection" form
    Then I should be at "home" page
    And I should see "inspection editing success" message


  Scenario: Incorrect Inspection editing
    Given I logged in as "root"
    And I open "inspection_edit" page with pk "1"
    And I select "" from "assigned_to"
    When I submit "inspection" form
    Then I should be at "inspection_edit" page with pk "1"
    And I should see "inspection editing error" message
    And I should see "This field is required." validation error message on field "assigned_to"