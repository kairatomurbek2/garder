Feature: Authorization

    Scenario Outline: Authorization
        Given Opened login page
        When I login as <role>
        Then I <reaction> - <site> on page
    Examples:
        | role     | reaction   | site        |
        | root     | see        | First Site  |
        | root     | see        | Second Site |
        | admin    | see        | Second Site |
        | admin    | do not see | First Site  |
        | surveyor | see        | First Site  |
        | surveyor | do not see | Second Site |
        | tester   | see        | Second Site |
        | tester   | do not see | First Site  |