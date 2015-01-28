Feature: Customer List

    Scenario Outline: Customer List page access
        Given I open "login" page
        And I login as "<role>"
        When I open "customer_list" page
        Then I should <reaction> following "<text>"

    Examples:
        | role     | reaction | text                       |
        | root     | see      | Gabe Newell :: Giles Corey |
        | root     | not see  | Not Found                  |
        | admin    | see      | Gabe Newell :: Giles Corey |
        | admin    | not see  | Not Found                  |
        | surveyor | see      | Not Found                  |
        | tester   | see      | Not Found                  |