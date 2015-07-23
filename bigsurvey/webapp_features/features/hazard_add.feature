@hazard_add
Feature: Hazard Add
  @keep_db
  Scenario Outline: Hazard Add page access
    Given I logged in as "<role>"
    When I directly open "hazard_add" page for site with pk "<pk>" and service "<service>"
    Then I should <reaction> "Page not found"

    Examples:
      | role     | pk | service | reaction |
      | root     | 1  | potable | not see  |
      | root     | 5  | fire    | not see  |
      | root     | 10 | potable | not see  |
      | admin    | 5  | fire    | see      |
      | admin    | 10 | potable | not see  |
      | admin    | 10 | fire    | not see  |
      | surveyor | 10 | potable | not see  |
      | surveyor | 10 | fire    | not see  |
      | surveyor | 5  | potable | see      |
      | tester   | 5  | potable | see      |
      | tester   | 10 | potable | see      |


  Scenario: Correct hazard adding
    Given I logged in as "root"
    When I directly open "hazard_add" page for site with pk "5" and service "fire"
    And I fill in following fields with following values
      | field     | value    |
      | location1 | backyard |
    And I select "Ice Maker" from "hazard_type"
    And I select "Yes" from "pump_present"
    And I select "Yes" from "additives_present"
    And I select "Yes" from "cc_present"
    And I select "Yes" from "aux_water"
    And I submit "hazard" form
    Then I should be at "hazard_detail" page with pk "4"
    And I should see "hazard adding success" message
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
    When I directly open "hazard_add" page for site with pk "5" and service "fire"
    And I submit "hazard" form
    Then I should be at "hazard_add" page for survey with pk "5" and service "fire"
    And I should see "hazard adding error" message
    And I should see following validation error messages on following fields
      | field       | error_message          |
      | hazard_type | This field is required |