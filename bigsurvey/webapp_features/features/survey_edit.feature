@survey_edit
Feature: Survey Edit
  @keep_db
  Scenario Outline: Survey Edit page access
    Given I logged in as "<role>"
    When I directly open "survey_edit" page with pk "<pk>"
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


  Scenario: Correct survey editing
    Given I logged in as "root"
    When I open "survey_edit" page with pk "1"
    And I fill in following fields with following values
      | field              | value      |
      | survey-survey_date | 2015-02-28 |
    And I select "Initial" from "survey-survey_type"
    And I submit survey form
    Then I should be at "survey_detail" page with pk "1"
    And I should see "survey editing success" message
    And I should see following
      | text          |
      | Feb. 28, 2015 |


  Scenario: Incorrect survey editing
    Given I logged in as "root"
    When I open "survey_edit" page with pk "1"
    And I fill in following fields with following values
      | field              | value |
      | survey-survey_date |       |
    And I submit survey form
    Then I should be at "survey_edit" page with pk "1"
    And I should see following validation error messages on following fields
      | field              | error_message          |
      | survey-survey_date | This field is required |