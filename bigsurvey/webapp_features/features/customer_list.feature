@customer_list
Feature: Customer list

    Scenario Outline: Customer list page access
        Given I open "login" page
        And I login as "<role>"
        When I open "customer list" page
        Then I should <reaction> "Not Found"
        And I log out
    Examples:
        | role     | reaction |
        | root     | not see  |
        | admin    | not see  |
        | surveyor | see      |
        | tester   | see      |


    Scenario: Root is opening customer list page
        Given I open "login" page
        And I login as "root"
        When I open "customer list" page
        Then I should see following
            | text          |
            | John Smith    |
            | Mike Doe      |
            | Amanda James  |
            | Jane Asperson |
            | Matt Asperson |
            | Giles Corey   |
            | Gabe Newell   |


    Scenario: Admin is opening customer list page
        Given I open "login" page
        And I login as "admin"
        When I open "customer list" page
        Then I should see following
            | text          |
            | John Smith    |
            | Mike Doe      |
            | Amanda James  |
            | Jane Asperson |
            | Matt Asperson |
            | Giles Corey   |
            | Gabe Newell   |