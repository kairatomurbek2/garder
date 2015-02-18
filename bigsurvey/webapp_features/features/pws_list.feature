@pws_list
Feature: PWS list

  Scenario Outline: PWS list page access
    Given I logged in as "<role>"
    When I directly open "pws_list" page
    Then I should <reaction> "Not Found"
    And I logout
  Examples:
    | role     | reaction |
    | root     | not see  |
    | admin    | see      |
    | surveyor | see      |
    | tester   | see      |


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