@inspection_add
Feature: Inspection adding


  Scenario Outline: Inspection adding page access
    Given I logged in as "<role>"
    When I directly open "inspection_add" page for site with pk "<pk>"
    Then I should <reaction> "Not Found"
    And I logout
  Examples:
    | role     | pk | reaction |
    | root     | 1  | not see  |
    | root     | 10 | not see  |
    | admin    | 1  | see      |
    | admin    | 10 | not see  |
    | surveyor | 1  | see      |
    | surveyor | 10 | see      |
    | tester   | 1  | see      |
    | tester   | 10 | see      |


  Scenario: Correct Inspection adding
    Given I logged in as "root"
    And I open "inspection_add" page for site with pk "1"
    And I select "surveyor_without_pws" from "assigned_to"
    When I submit "inspection" form
    Then I should be at "home" page
    And I should see "inspection adding success" message


  Scenario: Incorrect Inspection adding
    Given I logged in as "root"
    And I open "inspection_add" page for site with pk "1"
    When I submit "inspection" form
    Then I should be at "inspection_add" page for site with pk "1"
    And I should see "inspection adding error" message
    And I should see "This field is required." validation error message on field "assigned_to"

  Scenario: "Assigned to" list contains only Surveyors
    Given I logged in as "root"
    When I open "inspection_add" page for site with pk "1"
    Then I should see following options in following selects
      | option               | select      |
      | surveyor             | assigned_to |
      | surveyor_without_pws | assigned_to |
    And I should not see following options in following selects
      | option             | select      |
      | root               | assigned_to |
      | superadmin         | assigned_to |
      | admin              | assigned_to |
      | tester             | assigned_to |
      | tester_without_pws | assigned_to |