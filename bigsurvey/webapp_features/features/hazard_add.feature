@hazard_add
Feature: Hazard Add

  Scenario Outline: Hazard Add page access
    Given I logged in as "<role>"
    When I open "hazard add" page for survey with pk "<pk>"
    Then I should <reaction> "Not Found"
    And I logout

  Examples:
    | role     | pk | reaction |
    | root     | 1  | not see  |
    | root     | 2  | not see  |
    | admin    | 1  | see      |
    | admin    | 2  | not see  |
    | surveyor | 1  | see      |
    | surveyor | 2  | not see  |
    | tester   | 1  | see      |
    | tester   | 2  | see      |


  Scenario: Correct hazard adding
    Given I logged in as "root"
    When I open "hazard add" page for survey with pk "1"
    And I fill in following fields with following values
      | field       | value      |
      | location1   | backyard   |
    And I select "Ice Maker" from "hazard_type"
    And I submit "hazard" form
    Then I should be at "hazard detail" page with pk "4"
    And I should see "hazard adding success" message
    And I should see following
      | text     |
      | backyard |


  Scenario: Incorrect hazard adding
    Given I logged in as "root"
    When I open "hazard add" page for survey with pk "1"
    And I submit "hazard" form
    Then I should be at "hazard add" page for survey with pk "1"
    And I should see "hazard adding error" message
    And I should see following validation error messages on following fields
      | field       | error_message          |
      | hazard_type | This field is required |