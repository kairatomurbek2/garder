Feature: Customer Edit

    Scenario: Customer Edit
        Given I open "login" page
        And I login as "root"
        And I open "customer_edit" page with params "4"
        And I fill in "number" with "SUPERNUMBER"
        When I submit "customer" form
        Then I should be at "customer_list" page
        And I should see "SUPERNUMBER"

    Scenario: Customer Edit with errors
        Given I open "login" page
        And I login as "root"
        And I open "customer_edit" page with params "4"
        And I fill in "number" with ""
        When I submit "customer" form
        Then I should be at "customer_edit" page with params "4"
        And I should see "This field is required"