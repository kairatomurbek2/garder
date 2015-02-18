@testpermission_add
Feature: Test Permission adding


  Scenario Outline: Test Permission adding page access
    Given I logged in as "<role>"
    When I open "testpermission add" page for site with pk "<pk>"
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


  Scenario: Correct Test Permission adding
    Given I logged in as "root"
    And I open "testpermission add" page for site with pk "1"
    And I select "tester_without_pws" from "given_to"
    And I fill in "due_date" with "2015-06-01"
    When I submit "testpermission" form
    Then I should be at "home" page
    And I should see "testpermission adding success" message


  Scenario: Incorrect Test Permission adding
    Given I logged in as "root"
    And I open "testpermission add" page for site with pk "1"
    And I fill in "due_date" with "not a valid date"
    When I submit "testpermission" form
    Then I should be at "testpermission add" page for site with pk "1"
    And I should see "testpermission adding error" message
    And I should see following validation error messages on following fields
      | field    | error_message           |
      | given_to | This field is required. |
      | due_date | Enter a valid date.     |

  Scenario: "Given to" list contains only Testers
    Given I logged in as "root"
    When I open "testpermission add" page for site with pk "1"
    Then I should see following options in following selects
      | option             | select   |
      | tester             | given_to |
      | tester_without_pws | given_to |
    And I should not see following options in following selects
      | option               | select   |
      | root                 | given_to |
      | superadmin           | given_to |
      | admin                | given_to |
      | surveyor             | given_to |
      | surveyor_without_pws | given_to |