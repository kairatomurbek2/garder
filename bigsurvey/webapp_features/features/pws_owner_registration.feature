Feature: PWS Owner Registration

    Scenario: PWS Owner Registration page
        Given I register as PWS owner with following data
            | field                   | value                   |
            | pws_form-number         | LL9985452121            |
            | pws_form-name           | It attractor            |
            | pws_form-county         | Autauga County          |
            | pws_form-city           | Sitka                   |
            | pws_form-office_address | 111 First St            |
            | pws_form-zip            | 10007                   |
            | pws_form-phone          | +996700139680           |
            | user_form-first_name    | John                    |
            | user_form-last_name     | Smith                   |
            | user_form-email         | pwsowneremail@gmail.com |
            | user_form-username      | EastBoy                 |
            | user_form-password1     | password                |
            | user_form-password2     | password                |
        And I authenticate with "EastBoy" "password"
        Then I See the list of following sites

    Scenario: Payment for demo trial
        Given The system has data for the demo trial
        And I authenticate with "EastBoy" "password"
        And I click Pay and activate button
        And I click "payment_creation" link
        And I wait until step 2 is appeared
        And I click "approval" link
        And I login in PayPal
        And I confirm payment
        Then I should be redirected to "site" page
        And I should see "payment was completed successfully" message