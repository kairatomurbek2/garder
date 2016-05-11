@aa_group
Feature: Administrative Authority Group

  @keep_db
  Scenario Outline: Page access
    Given I logged in as "adauth"
    When I directly open "<page>" page
    Then I should <reaction> "Page not found"

    Examples:
      | page        | reaction |
      | site_list   | see      |
      | hazard_list | see      |
      | survey_list | see      |
      | test_list   | see      |
      | user_list   | see      |
      | pws_list    | not see  |
      | letter_list | see      |
      | tester_list | see      |


  @keep_db
  Scenario Outline: Pages with pk access
    Given I logged in as "adauth"
    When I directly open "<page>" page with pk "<pk>"
    Then I should <reaction> "Page not found"

    Examples:
      | page          | pk | reaction |
      | site_detail   | 1  | see      |
      | site_edit     | 1  | see      |
      | hazard_detail | 1  | see      |
      | hazard_edit   | 1  | see      |
      | survey_detail | 1  | see      |
      | survey_edit   | 1  | see      |
      | test_detail   | 1  | see      |
      | test_edit     | 1  | see      |