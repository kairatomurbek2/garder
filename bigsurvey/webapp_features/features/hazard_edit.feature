@hazard_edit
Feature: Hazard Edit

  Scenario Outline: Hazard Edit page access
    Given I logged in as "<role>"
    When I directly open "hazard_edit" page with pk "<pk>"
    Then I should <reaction> "Page not found"

    Examples:
      | role     | pk | reaction |
      | root     | 1  | not see  |
      | root     | 2  | not see  |
      | admin    | 2  | not see  |
      | admin    | 1  | see      |
      | surveyor | 2  | not see  |
      | surveyor | 1  | see      |
      | tester   | 2  | not see  |
      | tester   | 1  | not see  |


  Scenario: Tester Field Set
    Given I logged in as "tester"
    When I directly open "hazard_edit" page with pk "2"
    Then I should not see following
      | text        |
      | Hazard Type |
      | Location 1  |
      | Location 2  |
      | Notes       |

  Scenario Outline: Testing has_licence_for_installation property
    Given "tester" <relation> licence for installation
    And I logged in as "tester"
    When I directly open "hazard_edit" page with pk "2"
    Then I should <reaction> "Page not found"
    Examples:
      | relation      | reaction |
      | has           | not see  |
      | does not have | see      |

  Scenario: Correct hazard editing
    Given I logged in as "tester"
    When I directly open "hazard_edit" page with pk "2"
    And I fill in following fields with following values
      | field     | value |
      | installer | self  |
    And I select "Horizontal" from "orientation"
    And I select "Yes" from "pump_present"
    And I select "Yes" from "additives_present"
    And I select "Yes" from "cc_present"
    And I select "Yes" from "aux_water"
    And I submit "hazard" form
    Then I should be at "hazard_detail" page with pk "2"
    And I should see "hazard editing success" message
    And I should see following
      | text              |
      | self              |
      | Horizontal        |
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
    And I submit "hazard" form
    Then I should be at "hazard_edit" page with pk "1"
    And I should see "hazard editing error" message
    And I should see following validation error messages on following fields
      | field       | error_message          |
      | hazard_type | This field is required |