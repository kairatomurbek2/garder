@survey_detail
Feature: Survey Detail
  @keep_db
  Scenario Outline: Survey detail page access
    Given I logged in as "<role>"
    When I directly open "survey_detail" page with pk "<pk>"
    Then I should <reaction> "Page not found"

  Examples:
    | role      | pk | reaction |
    | root      | 1  | not see  |
    | root      | 2  | not see  |
    | admin     | 1  | see      |
    | admin     | 2  | not see  |
    | surveyor  | 1  | see      |
    | surveyor  | 2  | not see  |
    | tester    | 1  | see      |
    | tester    | 2  | see      |
    | root      | 3  | not see  |
    | admin     | 3  | see      |
    | surveyor  | 3  | see      |
    | tester    | 3  | see      |
    | pws_owner | 1  | not see  |
    | pws_owner | 2  | not see  |
    | pws_owner | 3  | see      |

  @keep_db
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