@hazard_edit
Feature: Hazard Edit

  Scenario Outline: Hazard Edit page access
    Given I logged in as "<role>"
    When I open "hazard edit" page with pk "<pk>"
    Then I should <reaction> "Not Found"
    And I logout

  Examples:
    | role     | pk | reaction |
    | root     | 1  | not see  |
    | root     | 2  | not see  |
    | admin    | 1  | not see  |
    | admin    | 2  | see      |
    | surveyor | 1  | not see  |
    | surveyor | 2  | see      |
    | tester   | 1  | not see  |
    | tester   | 2  | see      |


  Scenario: Tester Field Set
    Given I logged in as "tester"
    When I open "hazard edit" page with pk "1"
    Then I should not see following
      | text        |
      | Hazard Type |
      | Location 1  |
      | Location 2  |
      | Notes       |


  Scenario: Correct hazard editing
    Given I logged in as "tester"
    When I open "hazard edit" page with pk "1"
    And I fill in following fields with following values
      | field     | value |
      | installer | self  |
    And I select "Horizontal" from "orientation"
    And I submit "hazard" form
    Then I should be at "hazard detail" page with pk "1"
    And I should see "hazard editing success" message
    And I should see following
      | text       |
      | self       |
      | Horizontal |
      | Digester   |
      | Seattle    |


  Scenario: Incorrect hazard editing
    Given I logged in as "root"
    When I open "hazard edit" page with pk "1"
    And I select "---------" from "hazard_type"
    And I submit "hazard" form
    Then I should be at "hazard edit" page with pk "1"
    And I should see "hazard editing error" message
    And I should see following validation error messages on following fields
      | field       | error_message          |
      | hazard_type | This field is required |