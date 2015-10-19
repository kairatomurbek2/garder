@authorization
Feature: Authorization

  @keep_db
  Scenario Outline: Authorization with existent account
    Given I open "login" page
    When I login as "<role>"
    Then I should be at "<page>" page
  Examples:
    | role     | page        |
    | root     | home        |
    | admin    | home        |
    | surveyor | home        |
    | tester   | tester home |

  @keep_db
  @auth_non_exist
  Scenario: Authorization with non-existent account
    Given I open "login" page
    When I login as "non existent user"
    Then I should be at "login" page
    And I should see "Your Username and password didn't match. Please try again."