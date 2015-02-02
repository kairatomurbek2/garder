Feature: Site adding


    Scenario Outline: Site adding page access
        Given I open "login" page
        And I login as "<role>"
        When I open "site add" page
        Then I should <reaction> "Not Found"
    Examples:
        | role     | reaction |
        | root     | not see  |
        | admin    | not see  |
        | surveyor | see      |
        | tester   | see      |


    Scenario: Correct site adding
        Given I open "login" page
        And I login as "root"
        And I open "site add" page
        And I fill in following fields with following values
            | field        | value               |
            | connect_date | 2015-01-30          |
            | city         | Moscow              |
            | zip          | 000000              |
            | address1     | Red Square, Cremlin |
        And I select "Mike Doe" from "customer"
        And I select "Houston PWS" from "pws"
        And I select "Idaho" from "state"
        And I select "Agricultural" from "site_use"
        And I select "Grocery Store" from "site_type"
        And I select "2" from "floors"
        And I select "Yard" from "interconnection_point"
        When I submit "site" form
        Then I should be at "site list" page
        And I should see "site adding success" message
        And I should see following
            | text                |
            | Moscow              |
            | Red Square, Cremlin |
            | Mike Doe            |
            | Houston PWS         |
            | Agricultural        |
            | Grocery Store       |


    Scenario: Incorrect site adding
        Given I open "login" page
        And I login as "root"
        And I open "site add" page
        And I fill in "connect_date" with "not a valid date"
        When I submit "site" form
        Then I should be at "site add" page
        And I should see "site adding error" message
        And I should see following validation error messages on following fields
            | field                 | error_message           |
            | customer              | This field is required. |
            | connect_date          | Enter a valid date.     |
            | city                  | This field is required. |
            | state                 | This field is required. |
            | zip                   | This field is required. |
            | address1              | This field is required. |