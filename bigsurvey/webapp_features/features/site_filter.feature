Feature: Filtration


    Scenario: Filtration by city field while logged in as root
        Given I open "login" page
        And I login as "root"
        And I open "site list" page
        When I fill in "city" with "on"
        And I submit "site_filter" form
        Then I should see following
            | text        |
            | Second Site |
            | Houston     |
            | Boston      |
            | Washington  |
        And I should not see following
            | text        |
            | Ancoridge   |
            | New York    |
            | Los Angeles |


    Scenario: Filtration by address1 field while logged in as root
        Given I open "login" page
        And I login as "root"
        And I open "site list" page
        When I fill in "address1" with "cent"
        And I submit "site_filter" form
        Then I should see following
            | text      |
            | Ancoridge |
        And I should not see following
            | text        |
            | Houston     |
            | Boston      |
            | Washington  |
            | New York    |
            | Los Angeles |


    Scenario: Filtration by site_use field while logged in as admin
        Given I open "login" page
        And I login as "admin"
        And I open "site list" page
        When I fill in "site_use" with "ind"
        And I submit "site_filter" form
        Then I should see following
            | text    |
            | Chikago |
        And I should not see following
            | text        |
            | Houston     |
            | Boston      |
            | Washington  |
            | New York    |
            | Los Angeles |


    Scenario: Filtration by pws field while logged in as surveyor
        Given I open "login" page
        And I login as "surveyor"
        And I open "site list" page
        When I fill in "pws" with "north"
        And I submit "site_filter" form
        Then I should see following
            | text    |
            | Seattle |
        And I should not see following
            | text    |
            | Chikago |


    Scenario: Filtration by site_type field while logged in as tester
        Given I open "login" page
        And I login as "tester"
        And I open "site list" page
        When I fill in "site_type" with "govern"
        And I submit "site_filter" form
        Then I should see following
            | text     |
            | New York |
        And I should not see following
            | text       |
            | Washington |


    Scenario: Filtration by city and customer fields while logged in as root
        Given I open "login" page
        And I login as "root"
        And I open "site list" page
        When I fill in following fields with following values
            | field    | value |
            | city     | on    |
            | customer | matt  |
        And I submit "site_filter" form
        Then I should see following
            | text   |
            | Boston |


    Scenario: Filtration by city and customer fields while logged in as root
        Given I open "login" page
        And I login as "root"
        And I open "site list" page
        When I fill in following fields with following values
            | field    | value |
            | city     | chik  |
            | site_use | indus |
        And I submit "site_filter" form
        Then I should see following
            | text        |
            | Giles Corey |