Feature: PWS Add

    Scenario: PWS Add
        Given I open "login" page
        And I login as "root"
        And I open "pws_add" page
        When I fill in "number" with "PWS123456"
        And I fill in "name" with "My Super PWS"
        And I fill in "city" with "Bishkek"
        And I fill in "notes" with "Hello, world!"
        And I select "Private Well" from "water_source"
        And I submit "pws" form
        Then I should be at "pws_list" page
        And I should see "My Super PWS"

    Scenario: PWS Add with errors
        Given I open "login" page
        And I login as "root"
        And I open "pws_add" page
        When I submit "pws" form
        Then I should be at "pws_add" page
        And I should see "This field is required"