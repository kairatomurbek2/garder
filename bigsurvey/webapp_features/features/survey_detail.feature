@survey_detail
Feature: Survey Detail

  Scenario Outline: Survey detail page access
    Given I logged in as "<role>"
    When I directly open "survey_detail" page with pk "<pk>"
    Then I should <reaction> "Page not found"
    And I logout

  Examples:
    | role     | pk | reaction |
    | root     | 1  | not see  |
    | root     | 2  | not see  |
    | admin    | 1  | see      |
    | admin    | 2  | not see  |
    | surveyor | 1  | see      |
    | surveyor | 2  | not see  |
    | tester   | 1  | see      |
    | tester   | 2  | see      |


  Scenario: Survey detail page elements
    Given I logged in as "root"
    When I open "survey_detail" page with pk "1"
    Then I should see following
      | text         |
      | Service Type |
      | Surveyor     |
      | Metered      |
      | Hazards      |
      | Detail       |
      | Edit         |
      | Back to Site |