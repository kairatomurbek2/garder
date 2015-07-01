@survey_add

Feature: Survey Add

  Scenario Outline: Survey Add page access
    Given I logged in as "<role>"
    When I directly open "survey_add" page for site with pk "<pk>" and service "<service>"
    Then I should <reaction> "Page not found"
    And I logout

  Examples:
    | role     | pk | service    | reaction |
    | root     | 5  | potable    | not see  |
    | root     | 5  | irrigation | not see  |
    | admin    | 5  | potable    | see      |
    | admin    | 10 | potable    | not see  |
    | admin    | 10 | fire       | not see  |
    | surveyor | 10 | irrigation | not see  |
    | surveyor | 5  | potable    | see      |
    | surveyor | 2  | potable    | see      |
    | tester   | 10 | potable    | see      |

  @wip
  Scenario: Correct survey adding
    Given I logged in as "root"
    When I open "survey_add" page for site with pk "5" and service "potable"
    And I fill in following fields with following values
      | field       | value      |
      | survey_date | 2015-03-15 |
    And I select "Initial" from "survey_type"
    And I click "add_hazard" link
    And I select "Church Rec Center" from "hazard_type"
    And I fill in following fields with following values
      | field     | value |
      | latitude  | 10    |
      | longitude | -25   |
    Then Marker should be at "10" latitude and "-25" longitude
    And I submit "hazard" form
    And I close hazard modal
    And I submit "survey" form
    And I should see "survey adding success" message
    And I should see following
      | text              |
      | March 15, 2015    |
      | Church Rec Center |


  Scenario: Incorrect survey adding
    Given I logged in as "root"
    When I open "survey_add" page for site with pk "5" and service "potable"
    And I submit "survey" form
    Then I should be at "survey_add" page for site with pk "5" and service "potable"
    And I should see "survey adding error" message
    And I should see following validation error messages on following fields
      | field       | error_message          |
      | survey_date | This field is required |