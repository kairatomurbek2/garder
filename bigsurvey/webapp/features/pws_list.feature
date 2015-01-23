Feature: PWS List

    Scenario Outline: PWS List page access
        Given I open "login" page
        And I login as "<role>"
        When I open "pws_list" page
        Then I should <reaction> "<text>"

    Examples:
        | role     | reaction | text       |
        | root     | see      | PWS1       |
        | root     | see      | Show notes |
        | root     | not see  | Not Found  |
        | admin    | see      | Not Found  |
        | surveyor | see      | Not Found  |
        | tester   | see      | Not Found  |