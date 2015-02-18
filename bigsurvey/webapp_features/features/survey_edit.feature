@survey_edit
Feature: Survey Edit

  Scenario Outline: Survey Edit page access
    Given I logged in as "<role>"
    When I directly open "survey_edit" page with pk "<pk>"
    Then I should <reaction> "Not Found"
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


  Scenario: Correct survey editing
    Given I logged in as "root"
    When I open "survey_edit" page with pk "1"
    And I fill in following fields with following values
      | field       | value      |
      | survey_date | 2015-02-28 |
    And I select "Initial" from "survey_type"
    And I submit "survey" form
    Then I should be at "survey_detail" page with pk "1"
    And I should see "survey editing success" message
    And I should see following
      | text          |
      | Feb. 28, 2015 |


  Scenario: Incorrect survey editing
    Given I logged in as "root"
    When I open "survey_edit" page with pk "1"
    And I fill in following fields with following values
      | field       | value |
      | survey_date |       |
    And I submit "survey" form
    Then I should be at "survey_edit" page with pk "1"
    And I should see "survey editing error" message
    And I should see following validation error messages on following fields
      | field       | error_message          |
      | survey_date | This field is required |