@authorization
Feature: Authorization


  Scenario Outline: Authorization with existent account
    Given I open "login" page
    When I login as "<role>"
    Then I should be at "<page>" page
    And I logout
  Examples:
    | role     | page        |
    | root     | home        |
    | admin    | home        |
    | surveyor | home        |
    | tester   | tester home |


  Scenario: Authorization with non-existent account
    Given I open "login" page
    When I login as "non existent user"
    Then I should be at "login" page
    And I should see "Your Username and password didn't match. Please try again."