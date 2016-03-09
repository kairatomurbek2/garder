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


  Scenario: Adding multiple Hazard in the survey bp device
    Given I logged in as "root"
    And I open "survey_add" page for site with pk "5" and service "potable"
    And I choose today in "survey-survey_date"
    And I select "surveyor" from "survey-surveyor"
    And I click "add_hazard" link
    And I select "Ice Maker" from "hazard-0-hazard_type"
    And I select "Installed" from "hazard-0-assembly_status"
    And I select "Yes" from "hazard-0-pump_present"
    And I select "Yes" from "hazard-0-additives_present"
    And I select "Air Gap" from "hazard-0-letter_type"
    And I select "Yes" from "hazard-0-cc_present"
    And I select "Yes" from "hazard-0-aux_water"
    And I select "AVB" from "bp-0-bp_type_present"
    And I select "Yes" from "bp-0-installed_properly"
    And I select "Ames" from "bp-0-manufacturer"
    And I select "Horizontal" from "bp-0-orientation"
    And I select "At Meter" from "bp-0-assembly_location"
    And I submit hazard adding form
    And I submit survey form
    Then I directly open "hazard_detail" page with pk "5"
    And I should see following
      | text                  |
      | Assembly Type Present |
      | Assembly Location     |
      | Manufacturer          |
      | Orientation           |
      | Horizontal            |

  Scenario: Adding a few Hazard in the survey and uncheck some added
    Given I logged in as "root"
    And I open "survey_add" page for site with pk "8" and service "potable"
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
    And I click "add_hazard" link
    And I fill in following fields with following values
      | field              | value    |
      | hazard-1-location1 | backyard |
    And I select "Ice Maker" from "hazard-1-hazard_type"
    And I select "Yes" from "hazard-1-pump_present"
    And I select "Yes" from "hazard-1-additives_present"
    And I select "Yes" from "hazard-1-cc_present"
    And I select "Yes" from "hazard-1-aux_water"
    And I one submit hazard adding form
    And I click "add_hazard" link
    And I fill in following fields with following values
      | field              | value    |
      | hazard-2-location1 | backyard |
    And I select "Ice Maker" from "hazard-2-hazard_type"
    And I select "Yes" from "hazard-2-pump_present"
    And I select "Yes" from "hazard-2-additives_present"
    And I select "Yes" from "hazard-2-cc_present"
    And I select "Yes" from "hazard-2-aux_water"
    And I two submit hazard adding form
    And I click "add_hazard" link
    And I fill in following fields with following values
      | field              | value    |
      | hazard-3-location1 | backyard |
    And I select "Ice Maker" from "hazard-3-hazard_type"
    And I select "Yes" from "hazard-3-pump_present"
    And I select "Yes" from "hazard-3-additives_present"
    And I select "Yes" from "hazard-3-cc_present"
    And I select "Yes" from "hazard-3-aux_water"
    And I three submit hazard adding form
    And I uncheck "id_survey-hazards_0"
    And I uncheck "id_survey-hazards_3"
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
    Then I directly open "hazard_detail" page with pk "6"
    And I should see following
      | text              |
      | backyard          |
      | Pump Present      |
      | CC Present        |
      | Additives Present |
      | Auxiliary Water   |
      | Yes               |