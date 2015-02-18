@inspection_list
Feature: Inspection list

  Scenario Outline: Inspection list page access
    Given I logged in as "<role>"
    When I directly open "inspection_list" page
    Then I should <reaction> "Not Found"
    And I logout
  Examples:
    | role     | reaction |
    | root     | not see  |
    | admin    | not see  |
    | surveyor | see      |
    | tester   | see      |


  Scenario: Root is opening Inspection list page
    Given I logged in as "root"
    When I open "inspection_list" page
    Then I should see following
      | text                                |
      | First Site city, First Site address |
      | Seattle, 98, South Jackson st       |

  Scenario: Admin is opening Inspection list page
    Given I logged in as "admin"
    When I open "inspection_list" page
    Then I should see following
      | text                          |
      | Seattle, 98, South Jackson st |
    And I should not see following
      | text                                |
      | First Site city, First Site address |