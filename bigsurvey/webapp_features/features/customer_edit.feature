Feature: Customer editing


    Scenario Outline: Customer editing page access
        Given I open "login" page
        And I login as "<role>"
        When I open "customer edit" page with pk "4"
        Then I should <reaction> "Not Found"
    Examples:
        | role     | reaction |
        | root     | not see  |
        | admin    | not see  |
        | surveyor | see      |
        | tester   | see      |


    Scenario: Correct customer editing
        Given I open "login" page
        And I login as "root"
        And I open "customer edit" page with pk "4"
        And I fill in following fields with following values
            | field  | value   |
            | number | QAZ2WSX |
        When I submit "customer" form
        Then I should be at "customer list" page
        And I should see "customer editing success" message
        And I should see "QAZ2WSX"


    Scenario: Incorrect customer editing
        Given I open "login" page
        And I login as "root"
        And I open "customer edit" page with pk "4"
        And I fill in "number" with ""
        When I submit "customer" form
        Then I should be at "customer edit" page with pk "4"
        And I should see "customer editing error" message
        And I should see "This field is required." validation error message on field "number"