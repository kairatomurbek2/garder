Feature: PWS list

    Scenario Outline: PWS list page access
        Given I open "login" page
        And I login as "<role>"
        When I open "pws list" page
        Then I should <reaction> "Not Found"

    Examples:
        | role     | reaction |
        | root     | not see  |
        | admin    | see      |
        | surveyor | see      |
        | tester   | see      |


    Scenario: Root is opening PWS list page
        Given I open "login" page
        And I login as "root"
        When I open "pws list" page
        Then I should see following
            | text                     |
            | Houston PWS              |
            | Alaska Central PWS       |
            | White House PWS          |
            | Los Angeles Beach System |
            | MIT Public Water System  |
            | North USA PWS            |
            | South Western PWS        |