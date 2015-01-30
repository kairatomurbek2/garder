Feature: PWS editing


    Scenario Outline: PWS editing page access
        Given I open "login" page
        And I login as "<role>"
        When I open "pws edit" page with pk "6"
        Then I should <reaction> "Not Found"
    Examples:
        | role     | reaction |
        | root     | not see  |
        | admin    | see      |
        | surveyor | see      |
        | tester   | see      |


    Scenario: Correct PWS editing
        Given I open "login" page
        And I login as "root"
        And I open "pws edit" page with pk "6"
        And I fill in "notes" with "This is notes for PWS with id=6"
        When I submit "pws" form
        Then I should be at "pws list" page
        And I should see "This is notes for PWS with id=6"


    Scenario: Incorrect PWS editing
        Given I open "login" page
        And I login as "root"
        And I open "pws edit" page with pk "6"
        And I fill in "city" with ""
        When I submit "pws" form
        Then I should be at "pws edit" page with pk "6"
        And I should see "This field is required." validation error message on field "city"