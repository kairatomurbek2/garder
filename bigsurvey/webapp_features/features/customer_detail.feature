Feature: Customer Detail

    Scenario Outline: Customer Detail
        Given I open "login" page
        And I login as "<role>"
        When I open "customer_detail" page with params "<params>"
        Then I should <reaction> following "<text>"

    Examples:
        | role     | params | reaction | text                         |
        | root     | 3      | see      | SJK472 :: Ancoridge          |
        | root     | 7      | see      | 128, River Groove :: Chikago |
        | admin    | 3      | see      | SJK472 :: Ancoridge          |
        | surveyor | 3      | see      | Not Found                    |
        | tester   | 3      | see      | Not Found                    |