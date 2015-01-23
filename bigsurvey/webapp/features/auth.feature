Feature: Authorization

    Scenario Outline: Authorization
        Given I open "login" page
        When I login as "<role>"
        Then I should <reaction> "<site>"
    Examples:
        | role     | reaction | site        |
        | root     | see      | First Site  |
        | root     | see      | Second Site |
        | admin    | see      | Ancoridge   |
        | admin    | not see  | First Site  |
        | surveyor | see      | First Site  |
        | surveyor | not see  | Second Site |
        | tester   | see      | Second Site |
        | tester   | not see  | First Site  |