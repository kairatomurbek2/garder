Feature: PWS Edit

    Scenario: PWS Edit
        Given I open "login" page
        And I login as "root"
        And I open "pws_edit" page with params "6"
        And I fill in "notes" with "This is notes for PWS with id=6"
        And I submit "pws" form
        Then I should be at "pws_list" page
        And I should see "This is notes for PWS with id=6"

    Scenario: PWS Edit with errors
        Given I open "login" page
        And I login as "root"
        And I open "pws_edit" page with params "6"
        And I fill in "city" with ""
        When I submit "pws" form
        Then I should be at "pws_edit" page with params "6"
        And I should see "This field is required"