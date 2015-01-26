Feature: Authorization

    Scenario Outline: Authorization
        Given I open "login" page
        When I login as "<role>"
        Then I should <reaction> following "<text>"
    Examples:
        | role     | reaction | text                                                                     |
        | root     | see      | First Site :: Second Site :: Houston :: Ancoridge :: Seattle :: New York |
        | admin    | see      | Ancoridge :: Chikago :: Seattle                                          |
        | admin    | not see  | First Site :: Second Site :: Boston :: Houston :: Washington             |
        | surveyor | see      | First Site :: Seattle                                                    |
        | surveyor | not see  | Second Site :: Boston :: Houston :: Washington :: Ancoridge              |
        | tester   | see      | Second Site :: New York :: Seattle                                       |
        | tester   | not see  | First Site :: Boston :: Houston :: Washington :: Ancoridge               |