Feature: Authorization

    Scenario: Root authorization
        When I go to login page
        And Login as root
        Then I see First Site on page
        And I see Second Site on page

    Scenario: Admin authorization
        When I go to login page
        And Login as admin
        Then I see Second Site on page
        And I do not see First Site on page

    Scenario: Surveyor authorization
        When I go to login page
        And Login as surveyor
        Then I see First Site on page
        And I do not see Second Site on page

    Scenario: Tester authorization
        When I go to login page
        And Login as tester
        Then I see Second Site on page
        And I do not see First Site on page