@hazard_detail
Feature: Hazard Detail

  Scenario Outline: Hazard detail page access
    Given I logged in as "<role>"
    When I directly open "hazard_detail" page with pk "<pk>"
    Then I should <reaction> "Page not found"
    And I logout

  Examples:
    | role     | pk | reaction |
    | root     | 1  | not see  |
    | root     | 2  | not see  |
    | admin    | 2  | not see  |
    | admin    | 1  | see      |
    | surveyor | 2  | not see  |
    | surveyor | 1  | see      |
    | tester   | 2  | not see  |
    | tester   | 1  | not see  |


  Scenario: Hazard detail page elements
    Given I logged in as "root"
    When I open "hazard_detail" page with pk "1"
    Then I should see following
      | text                    |
      | Washington, White House |
      | irrigation              |
      | Digester                |
      | Location 1              |
      | Installer               |
      | Feb. 18, 2015           |
      | Edit                    |
      | Add Test                |
      | Jan. 27, 2015, Failed   |