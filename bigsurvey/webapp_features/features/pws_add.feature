@pws_add
Feature: PWS adding
  @keep_db
  Scenario Outline: PWS adding page access
    Given I logged in as "<role>"
    When I directly open "pws_add" page
    Then I should <reaction> "Page not found"
  Examples:
    | role     | reaction |
    | root     | not see  |
    | admin    | see      |
    | surveyor | see      |
    | tester   | see      |


  Scenario: Correct PWS adding
    Given I logged in as "root"
    And I open "pws_add" page
    And I fill in following fields with following values
      | field  | value     |
      | number | PWS123456 |
      | name   | NEW PWS   |
      | city   | Bishkek   |
      | price  | 13        |
    And I select "Private Well" from "water_source"
    When I submit "pws" form
    Then I should see "pws adding success" message
    And I should see "NEW PWS"
    And New letter types were created for PWS with number "PWS123456"


  Scenario: Incorrect PWS adding
    Given I logged in as "root"
    And I open "pws_add" page
    When I submit "pws" form
    Then I should be at "pws_add" page
    And I should see "pws adding error" message
    And I should see following validation error messages on following fields
      | field  | error_message           |
      | number | This field is required. |
      | name   | This field is required. |