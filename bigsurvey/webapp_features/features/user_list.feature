@user_list
Feature: User list

  @keep_db
  Scenario Outline: User list page access
    Given I logged in as "<role>"
    When I directly open "user_list" page
    Then I should <reaction> "Page not found"
  Examples:
    | role     | reaction |
    | root     | not see  |
    | admin    | not see  |
    | surveyor | see      |
    | tester   | see      |

  @keep_db
  Scenario: Root is opening user list page
    Given I logged in as "root"
    When I open "user_list" page
    Then I should see following
      | text                 |
      | root                 |
      | superadmin           |
      | admin                |
      | surveyor             |
      | tester               |
      | surveyor_without_pws |
      | tester_without_pws   |
  @keep_db
  Scenario: Admin is opening user list page
    Given I logged in as "admin"
    When I open "user_list" page
    Then I should see following
      | text     |
      | admin    |
      | surveyor |
      | tester   |
    And I should not see following
      | text                 |
      | root                 |
      | superadmin           |
      | surveyor_without_pws |
      | tester_without_pws   |
