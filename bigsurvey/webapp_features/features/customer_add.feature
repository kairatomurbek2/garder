Feature: Customer Add

    Scenario: Customer Add
        Given I open "login" page
        And I login as "root"
        And I open "customer_add" page
        And I fill in "number" with "CUST987"
        And I fill in "name" with "Ivan Ivanov"
        And I fill in "city" with "Bishkek"
        And I fill in "zip" with "123456789"
        And I fill in "address1" with "Wall Street"
        And I fill in "notes" with "Hello, world!"
        And I select "Fire" from "code"
        And I select "Kansas" from "state"
        When I submit "customer" form
        Then I should be at "customer_list" page
        And I should see "Ivan Ivanov"

    Scenario: Customer Add with errors
        Given I open "login" page
        And I login as "root"
        And I open "customer_add" page
        When I submit "customer" form
        Then I should be at "customer_add" page
        And I should see "This field is required"