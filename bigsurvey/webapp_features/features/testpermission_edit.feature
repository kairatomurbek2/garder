@testpermission_edit
Feature: Test Permission editing


  Scenario Outline: Test Permission editing page access
    Given I logged in as "<role>"
    When I open "testpermission edit" page with pk "<pk>"
    Then I should <reaction> "Not Found"
    And I logout
  Examples:
    | role     | pk | reaction |
    | root     | 1  | not see  |
    | root     | 3  | not see  |
    | admin    | 1  | see      |
    | admin    | 3  | not see  |
    | surveyor | 1  | see      |
    | surveyor | 3  | see      |
    | tester   | 1  | see      |
    | tester   | 3  | see      |


  Scenario: Correct Test Permission editing
    Given I logged in as "root"
    And I open "testpermission edit" page with pk "1"
    And I select "tester_without_pws" from "given_to"
    And I fill in "due_date" with "2016-01-01"
    When I submit "testpermission" form
    Then I should be at "home" page
    And I should see "testpermission editing success" message


  Scenario: Incorrect Test Permission editing
    Given I logged in as "root"
    And I open "testpermission edit" page with pk "1"
    And I select "" from "given_to"
    When I submit "testpermission" form
    Then I should be at "testpermission edit" page with pk "1"
    And I should see "testpermission editing error" message
    And I should see "This field is required." validation error message on field "given_to"