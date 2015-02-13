@survey_add
Feature: Survey Add

  Scenario Outline: Survey Add page access
    Given I logged in as "<role>"
    When I open "survey add" page for site with pk "<pk>" and service "<service>"
    Then I should <reaction> "Not Found"
    And I logout

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


  Scenario: Correct survey adding
    Given I logged in as "root"
    When I open "survey add" page for site with pk "5" and service "potable"
    And I fill in following fields with following values
      | field       | value      |
      | survey_date | 2015-03-15 |
    And I select "Initial" from "survey_type"
    And I submit "survey" form
    Then I should be at "survey detail" page with pk "3"
    And I should see "survey adding success" message
    And I should see following
      | text           |
      | March 15, 2015 |


  Scenario: Incorrect survey adding
    Given I logged in as "root"
    When I open "survey add" page for site with pk "5" and service "potable"
    And I submit "survey" form
    Then I should be at "survey add" page for site with pk "5" and service "potable"
    And I should see "survey adding error" message
    And I should see following validation error messages on following fields
      | field       | error_message          |
      | survey_date | This field is required |