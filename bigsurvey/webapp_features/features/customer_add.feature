@customer_add
Feature: Customer adding


    Scenario Outline: Customer adding page access
        Given I open "login" page
        And I login as "<role>"
        When I open "customer add" page
        Then I should <reaction> "Not Found"
        And I log out
    Examples:
        | role     | reaction |
        | root     | not see  |
        | admin    | not see  |
        | surveyor | see      |
        | tester   | see      |


    Scenario: Correct customer adding
        Given I open "login" page
        And I login as "root"
        And I open "customer add" page
        And I fill in following fields with following values
            | field    | value         |
            | number   | CUST987       |
            | name     | Ivan Ivanov   |
            | city     | Bishkek       |
            | zip      | 123456789     |
            | address1 | Hello, world! |
        And I select "Fire" from "code"
        And I select "Kansas" from "state"
        When I submit "customer" form
        Then I should be at "customer list" page
        And I should see "customer adding success" message
        And I should see following
            | text          |
            | CUST987       |
            | Ivan Ivanov   |
            | Bishkek       |
            | Hello, world! |


    Scenario: Incorrect customer adding
        Given I open "login" page
        And I login as "root"
        And I open "customer add" page
        When I submit "customer" form
        Then I should be at "customer add" page
        And I should see "customer adding error" message
        And I should see following validation error messages on following fields
            | field    | error_message           |
            | number   | This field is required. |
            | name     | This field is required. |
            | code     | This field is required. |
            | city     | This field is required. |
            | state    | This field is required. |
            | zip      | This field is required. |
            | address1 | This field is required. |