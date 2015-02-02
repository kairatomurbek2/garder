Feature: Site editing


    Scenario Outline: Site editing page access
        Given I open "login" page
        And I login as "<role>"
        When I open "site edit" page with pk "<pk>"
        Then I should <reaction> "Not Found"
    Examples:
        | role     | pk | reaction |
        | root     | 3  | not see  |
        | root     | 4  | not see  |
        | admin    | 3  | see      |
        | admin    | 4  | not see  |
        | surveyor | 3  | see      |
        | tester   | 3  | see      |


    Scenario: Correct site editing
        Given I open "login" page
        And I login as "root"
        And I open "site edit" page with pk "4"
        And I fill in following fields with following values
            | field    | value                |
            | address1 | 20/12 Central Square |
        When I submit "site" form
        Then I should be at "site list" page
        And I should see "site editing success" message
        And I should see "20/12 Central Square"


    Scenario: Incorrect site editing
        Given I open "login" page
        And I login as "root"
        And I open "site edit" page with pk "4"
        And I fill in "connect_date" with "qaz2wsx"
        When I submit "site" form
        Then I should be at "site edit" page with pk "4"
        And I should see "site editing error" message
        And I should see "Enter a valid date." validation error message on field "connect_date"