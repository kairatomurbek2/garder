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