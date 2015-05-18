@user_edit
Feature: User editing


  Scenario Outline: User editing page access
    Given I logged in as "<role>"
    When I directly open "user_edit" page with pk "<pk>"
    Then I should <reaction> "Page not found"
    And I logout
  Examples:
    | role     | pk | reaction |
    | root     | 3  | not see  |
    | root     | 10 | not see  |
    | admin    | 3  | not see  |
    | admin    | 10 | see      |
    | surveyor | 3  | see      |
    | surveyor | 10 | see      |
    | tester   | 3  | see      |
    | tester   | 10 | see      |


  Scenario: Correct user editing
    Given I logged in as "root"
    And I open "user_edit" page with pk "3"
    And I fill in following fields with following values
      | field      | value             |
      | first_name | New Surveyor Name |
    When I submit "user" form
    Then I should be at "user_list" page
    And I should see "user editing success" message
    And I should see "New Surveyor Name"


  Scenario: Incorrect user editing
    Given I logged in as "root"
    And I open "user_edit" page with pk "3"
    And I fill in following fields with following values
      | field     | value  |
      | username  | admin  |
      | password1 | 123456 |
    When I submit "user" form
    Then I should be at "user_edit" page with pk "3"
    And I should see "user editing error" message
    And I should see following validation error messages on following fields
      | field     | error_message                           |
      | username  | User with this Username already exists. |
      | password2 | The two password fields didn't match.   |