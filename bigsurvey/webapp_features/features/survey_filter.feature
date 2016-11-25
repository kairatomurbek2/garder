@survey
@survey_filter
Feature: Survey Filtration

  @keep_db
  Scenario: SurveyFiltration
    Given I logged in as "root"
    And I open "survey_list" page
    When I fill in following fields with following values
      | field            | value       |
      | customer         | QAZ2WSX     |
      | city             | Washington  |
      | address          | White House |
      | survey_date_from | 2015-01-26  |
      | survey_date_to   | 2015-01-26  |
    And I select "DOC121" from "pws"
    And I select "potable" from "service_type"
    And I select "Initial/Drive-by" from "survey_type"
    And I select "surveyor" from "surveyor"
    And I submit "survey_filter" form
    Then I should see following
      | text          |
      | QAZ2WSX       |
      | Jan. 26, 2015 |
    And I should not see following
      | text    |
      | Seattle |
      | VALVE   |