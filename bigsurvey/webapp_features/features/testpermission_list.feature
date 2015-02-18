@testpermission_list
Feature: Test Permission list

  Scenario Outline: Test Permission list page access
    Given I logged in as "<role>"
    When I directly open "testpermission_list" page
    Then I should <reaction> "Not Found"
    And I logout
  Examples:
    | role     | reaction |
    | root     | not see  |
    | admin    | not see  |
    | surveyor | see      |
    | tester   | see      |


  Scenario: Root is opening Test Permission list page
    Given I logged in as "root"
    When I open "testpermission_list" page
    Then I should see following
      | text                                  |
      | Second Site city, Second Site address |
      | New York, Manhattan                   |
      | Seattle, 98, South Jackson st         |

  Scenario: Admin is opening Test Permission list page
    Given I logged in as "admin"
    When I open "testpermission_list" page
    Then I should see following
      | text                          |
      | Seattle, 98, South Jackson st |
    And I should not see following
      | text                                  |
      | Second Site city, Second Site address |
      | New York, Manhattan                   |