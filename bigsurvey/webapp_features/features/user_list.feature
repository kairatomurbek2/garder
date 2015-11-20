@user
@user_list
Feature: User list

  @keep_db
  Scenario Outline: User list page access
    Given I logged in as "<role>"
    When I directly open "user_list" page
    Then I should <reaction> "Page not found"
  Examples:
    | role      | reaction |
    | root      | not see  |
    | admin     | not see  |
    | pws_owner | not see  |
    | surveyor  | see      |
    | tester    | see      |

  @keep_db
  Scenario: Root is opening user list page
    Given I logged in as "root"
    When I open "user_list" page
    Then I should see following user in following tab
      | user                 | tab |
      | root                 | 1   |
      | superadmin           | 1   |
      | owner                | 2   |
      | admin                | 3   |
      | surveyor             | 4   |
      | tester               | 5   |
      | surveyor_without_pws | 4   |
      | tester_without_pws   | 5   |
      | adauth               | 6   |

  @keep_db
  Scenario: Pws owner is opening user list page
    Given I logged in as "pws_owner"
    When I open "user_list" page
    Then I should see following user in following tab
      | user                 | tab |
      | owner                | 1   |
      | admin                | 2   |
      | surveyor             | 3   |
      | tester               | 4   |
      | pws6user             | 3   |
    And I should not see following user in any of 5 tabs
      | user                 |
      | root                 |
      | surveyor_without_pws |
      | tester_without_pws   |

  @keep_db
  Scenario: Admin is opening user list page
    Given I logged in as "admin"
    When I open "user_list" page
    Then I should see following user in following tab
      | user     | tab |
      | admin    | 1   |
      | surveyor | 2   |
      | tester   | 3   |
    And I should not see following user in any of 4 tabs
      | user                 |
      | root                 |
      | superadmin           |
      | surveyor_without_pws |
      | tester_without_pws   |
      | owner                |
