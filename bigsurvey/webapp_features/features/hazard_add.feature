@hazard_add
Feature: Hazard Add


  Scenario: Correct hazard adding
    Given I logged in as "root"
    And I open "survey_add" page for site with pk "5" and service "potable"
    And I choose today in "survey-survey_date"
    And I select "surveyor" from "survey-surveyor"
    And I click "add_hazard" link
    And I fill in following fields with following values
      | field              | value    |
      | hazard-0-location1 | backyard |
    And I select "Ice Maker" from "hazard-0-hazard_type"
    And I select "Yes" from "hazard-0-pump_present"
    And I select "Yes" from "hazard-0-additives_present"
    And I select "Yes" from "hazard-0-cc_present"
    And I select "Yes" from "hazard-0-aux_water"
    And I submit hazard adding form
    And I submit survey form
    Then I directly open "hazard_detail" page with pk "5"
    And I should see following
      | text              |
      | backyard          |
      | Pump Present      |
      | CC Present        |
      | Additives Present |
      | Auxiliary Water   |
      | Yes               |

  Scenario: Incorrect hazard adding
    Given I logged in as "root"
    And I open "survey_add" page for site with pk "5" and service "fire"
    And I choose today in "survey-survey_date"
    And I select "surveyor" from "survey-surveyor"
    And I click "add_hazard" link
    When I submit hazard adding form
    And I should see following validation error messages on following fields
      | field                | error_message          |
      | hazard-0-hazard_type | This field is required |