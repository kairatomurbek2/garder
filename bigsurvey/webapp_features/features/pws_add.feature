@pws_add
Feature: PWS adding


    Scenario Outline: PWS adding page access
        Given I open "login" page
        And I login as "<role>"
        When I open "pws add" page
        Then I should <reaction> "Not Found"
        And I log out
    Examples:
        | role     | reaction |
        | root     | not see  |
        | admin    | see      |
        | surveyor | see      |
        | tester   | see      |


    Scenario: Correct PWS adding
        Given I open "login" page
        And I login as "root"
        And I open "pws add" page
        And I fill in following fields with following values
            | field  | value     |
            | number | PWS123456 |
            | name   | NEW PWS   |
            | city   | Bishkek   |
        And I select "Private Well" from "water_source"
        When I submit "pws" form
        Then I should be at "pws list" page
        And I should see "pws adding success" message
        And I should see "NEW PWS"


    Scenario: Incorrect PWS adding
        Given I open "login" page
        And I login as "root"
        And I open "pws add" page
        When I submit "pws" form
        Then I should be at "pws add" page
        And I should see "pws adding error" message
        And I should see following validation error messages on following fields
            | field        | error_message           |
            | number       | This field is required. |
            | name         | This field is required. |