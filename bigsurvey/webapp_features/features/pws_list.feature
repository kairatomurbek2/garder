@pws
@pws_list
Feature: PWS list
  @keep_db
  Scenario Outline: PWS list page access
    Given I logged in as "<role>"
    When I directly open "pws_list" page
    Then I should <reaction> "Page not found"
  Examples:
    | role      | reaction |
    | root      | not see  |
    | pws_owner | not see  |
    | admin     | see      |
    | surveyor  | see      |
    | tester    | see      |

  @keep_db
  Scenario: Root is opening PWS list page
    Given I logged in as "root"
    When I open "pws_list" page
    Then I should see following
      | text                     |
      | Houston PWS              |
      | Alaska Central PWS       |
      | White House PWS          |
      | Los Angeles Beach System |
      | MIT Public Water System  |
      | North USA PWS            |
      | South Western PWS        |

  @keep_db
  Scenario: PWS owner is opening PWS list page
    Given I logged in as "pws_owner"
    When I open "pws_list" page
    Then I should see following
      | text                     |
      | White House PWS          |
      | North USA PWS            |
    And I should not see following
      | text                     |
      | Los Angeles Beach System |
      | MIT Public Water System  |
      | Houston PWS              |
      | Alaska Central PWS       |
      | South Western PWS        |