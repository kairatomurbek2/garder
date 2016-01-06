@survey_add
Feature: Survey Add
  @keep_db
  Scenario Outline: Survey Add page access
    Given I logged in as "<role>"
    When I directly open "survey_add" page for site with pk "<pk>" and service "<service>"
    Then I should <reaction> "Page not found"

  Examples:
    | role      | pk | service    | reaction |
    | root      | 5  | potable    | not see  |
    | root      | 5  | irrigation | not see  |
    | admin     | 5  | potable    | see      |
    | admin     | 10 | potable    | not see  |
    | admin     | 10 | fire       | not see  |
    | surveyor  | 10 | irrigation | not see  |
    | surveyor  | 5  | potable    | see      |
    | surveyor  | 2  | potable    | see      |
    | tester    | 10 | potable    | see      |
    | pws_owner | 2  | potable    | see      |
    | pws_owner | 5  | potable    | not see  |
    | pws_owner | 10 | potable    | not see  |

  @survey_add_correct
  Scenario: Correct survey adding
    Given I logged in as "root"
    And Site with pk "5" has "potable" service turned off
    When I open "survey_add" page for site with pk "5" and service "potable"
    And I fill in following fields with following values
      | field       | value      |
      | survey_date | 2015-03-15 |
    And I select "Initial" from "survey_type"
    And I click "add_hazard" link
    And I select "Church Rec Center" from "hazard_type"
    And I submit "hazard" form
    Then Site with pk "5" should have "potable" service turned on
    And I submit "survey" form
    And I should see "survey adding success" message
    And I should see following
      | text              |
      | March 15, 2015    |
      | Church Rec Center |

  @survey_manual_crds
  Scenario: Manual settings coordinates
    Given I logged in as "root"
    And Site with pk "5" has "potable" service turned off
    When I open "survey_add" page for site with pk "5" and service "potable"
    And I click "add_hazard" link
    And I fill in following fields with following values
      | field     | value |
      | latitude  | 10    |
      | longitude | -25   |
    Then Marker should be at "10" latitude and "-25" longitude

  @survey_geolocation_check
  Scenario: Geolocation check
    Given I logged in as "root"
    And Site with pk "5" has "potable" service turned off
    When I open "survey_add" page for site with pk "5" and service "potable"
    And I click "add_hazard" link
    And I click "get-location" button
    Then Marker should be approximately inside Bishkek


  Scenario: Incorrect survey adding
    Given I logged in as "root"
    When I open "survey_add" page for site with pk "5" and service "potable"
    And I submit "survey" form
    Then I should be at "survey_add" page for site with pk "5" and service "potable"
    And I should see "survey adding error" message
    And I should see following validation error messages on following fields
      | field       | error_message          |
      | survey_date | This field is required |


  Scenario Outline: NHP hazard is added automatically when no hazards were chosen
    Given I logged in as "root"
    When I submit survey form for site with pk "6" and service "<service>" without hazard
    Then On survey details page I see NHP hazard

  Examples:
    | service    |
    | potable    |
    | irrigation |
    | fire       |
