@user_add
Feature: User adding


  Scenario Outline: User adding page access
    Given I logged in as "<role>"
    When I open "user add" page
    Then I should <reaction> "Not Found"
    And I logout
  Examples:
    | role     | reaction |
    | root     | not see  |
    | admin    | not see  |
    | surveyor | see      |
    | tester   | see      |


  Scenario: Correct user adding
    Given I logged in as "root"
    And I open "user add" page
    And I fill in following fields with following values
      | field      | value               |
      | username   | newuser             |
      | email      | newuser@example.com |
      | first_name | John                |
      | last_name  | Smith               |
      | password1  | password            |
      | password2  | password            |
    And I select "Surveyor" from "groups"
    And I select "Alaska Central PWS" from "pws"
    When I submit "user" form
    Then I should be at "user list" page
    And I should see "user adding success" message
    And I should see following
      | text                |
      | newuser             |
      | newuser@example.com |
      | John                |
      | Smith               |
      | Alaska Central PWS  |


  Scenario: Incorrect user adding
    Given I logged in as "root"
    And I open "user add" page
    And I fill in "username" with "admin"
    When I submit "user" form
    Then I should be at "user add" page
    And I should see "user adding error" message
    And I should see following validation error messages on following fields
      | field     | error_message                             |
      | username  | A user with that username already exists. |
      | password1 | This field is required.                   |
      | password2 | This field is required.                   |