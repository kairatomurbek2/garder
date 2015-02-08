@customer_detail
Feature: Customer detail


    Scenario Outline: Customer detail page access
        Given I open "login" page
        And I login as "<role>"
        When I open "customer detail" page with pk "3"
        Then I should <reaction> "Not Found"
        And I log out
    Examples:
        | role     | reaction |
        | root     | not see  |
        | admin    | not see  |
        | surveyor | see      |
        | tester   | see      |


    Scenario: Root is opening customer detail page
        Given I open "login" page
        And I login as "root"
        When I open "customer detail" page with pk "3"
        Then I should see following
            | text       |
            | SJK472     |
            | Ancoridge  |
            | 10, New St |
            | Mike Doe   |
            | Industrial |
            | 29021      |


    Scenario: Admin is opening customer detail page
        Given I open "login" page
        And I login as "admin"
        When I open "customer detail" page with pk "7"
        Then I should see following
            | text              |
            | OIK182            |
            | Chikago           |
            | 128, River Groove |
            | Giles Corey       |
            | Governmental      |
            | 19021             |