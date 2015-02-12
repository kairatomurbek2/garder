@survey_edit
Feature: Survey Edit

  Scenario Outline: Survey Edit page access
    Given I open "login" page
    And I login as "<role>"
    When I open "survey add" page for site with pk "<pk>" and service "<service>"
    Then I should <reaction> "Not Found"
    And I log out

  Examples:
    | role     | pk | service    | reaction |
    | root     | 5  | potable    | not see  |
    | root     | 5  | irrigation | see      |
    | admin    | 5  | potable    | see      |
    | admin    | 10 | potable    | not see  |
    | admin    | 10 | fire       | see      |
    | surveyor | 10 | irrigation | not see  |
    | surveyor | 5  | potable    | see      |
    | surveyor | 2  | potable    | see      |
    | tester   | 10 | potable    | see      |


  Scenario: Correct survey editing
    Given I logged in as "root"
    When I open "survey edit" page with pk "1"
    And I fill in following fields with following values
    | field                 | value      |
    | survey_date           | 2015-02-28 |
    And I select "Initial" from "survey_type"
    And I submit "survey" form
    Then I should be at "survey detail" page with pk "1"
    And I should see "survey editing success" message
    And I should see following
    | text          |
    | Feb. 28, 2015 |


  Scenario: Incorrect survey editing
    Given I logged in as "root"
    When I open "survey edit" page with pk "1"
    And I fill in following fields with following values
    | field                 | value      |
    | survey_date           |            |
    And I submit "survey" form
    Then I should be at "survey edit" page with pk "1"
    And I should see "survey editing error" message
    And I should see following validation error messages on following fields
    | field       | error_message          |
    | survey_date | This field is required |