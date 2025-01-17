@hazard_edit
Feature: Hazard Edit

  @keep_db
  @hazard_access
  Scenario Outline: Hazard Edit page access
    Given I logged in as "<role>"
    When I directly open "hazard_edit" page with pk "<pk>"
    Then I should <reaction> "Page not found"

    Examples:
      | role      | pk | reaction |
      | root      | 1  | not see  |
      | root      | 2  | not see  |
      | root      | 4  | not see  |
      | admin     | 2  | not see  |
      | admin     | 1  | see      |
      | admin     | 4  | see      |
      | pws_owner | 1  | not see  |
      | pws_owner | 2  | not see  |
      | pws_owner | 4  | see      |
      | surveyor  | 2  | not see  |
      | surveyor  | 1  | see      |
      | surveyor  | 4  | see      |
      | tester    | 2  | see      |
      | tester    | 1  | see      |
      | tester    | 3  | see      |

  @correct_hazard_edit
  Scenario: Correct hazard editing
    Given I logged in as "admin"
    When I directly open "hazard_edit" page with pk "2"
    And I fill in following fields with following values
      | field | value          |
      | notes | this is hazard |
    And I select "Pollutant" from "hazard_degree"
    And I select "Yes" from "pump_present"
    And I select "Yes" from "additives_present"
    And I select "Yes" from "cc_present"
    And I select "Yes" from "aux_water"
    And I submit "hazard" form
    Then I should be at "hazard_detail" page with pk "2"
    And I should see "hazard editing success" message
    And I should see following
      | text              |
      | this is hazard    |
      | Pollutant         |
      | Trailer Park      |
      | Washington        |
      | Pump Present      |
      | CC Present        |
      | Additives Present |
      | Auxiliary Water   |
      | Yes               |


  Scenario: Incorrect hazard editing
    Given I logged in as "root"
    When I open "hazard_edit" page with pk "1"
    And I select "" from "hazard_type"
    And I submit hazard adding form
    Then I should be at "hazard_edit" page with pk "1"
    And I should see "hazard editing error" message
    And I should see following validation error messages on following fields
      | field       | error_message          |
      | hazard_type | This field is required |