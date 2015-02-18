@hazard_detail
Feature: Hazard Detail

  Scenario Outline: Hazard detail page access
    Given I logged in as "<role>"
    When I directly open "hazard_detail" page with pk "<pk>"
    Then I should <reaction> "Not Found"
    And I logout

  Examples:
    | role     | pk | reaction |
    | root     | 1  | not see  |
    | root     | 2  | not see  |
    | admin    | 1  | not see  |
    | admin    | 2  | see      |
    | surveyor | 1  | not see  |
    | surveyor | 2  | see      |
    | tester   | 1  | not see  |
    | tester   | 2  | see      |


  Scenario: Hazard detail page elements
    Given I logged in as "root"
    When I open "hazard_detail" page with pk "1"
    Then I should see following
      | text                  |
      | Site                  |
      | Survey                |
      | Location 1            |
      | Installer             |
      | Feb. 18, 2015         |
      | May 31, 2015          |
      | Edit                  |
      | Menu                  |
      | Add Test              |
      | Jan. 27, 2015, Failed |