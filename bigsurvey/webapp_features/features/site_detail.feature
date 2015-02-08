@site_detail
Feature: Site detail


    Scenario Outline: Site detail page access
        Given I open "login" page
        And I login as "<role>"
        When I open "site detail" page with pk "<pk>"
        Then I should <reaction> "Not Found"
        And I log out
    Examples:
        | role     | pk | reaction |
        | root     | 3  | not see  |
        | root     | 4  | not see  |
        | admin    | 3  | see      |
        | admin    | 4  | not see  |
        | surveyor | 3  | see      |
        | surveyor | 2  | not see  |
        | tester   | 3  | see      |
        | tester   | 6  | not see  |


    Scenario: Root is opening site detail page
        Given I open "login" page
        And I login as "root"
        When I open "site detail" page with pk "10"
        Then I should see following
            | text            |
            | Gabe Newell     |
            | Assign Surveyor |
            | Assign Tester   |
            | Edit            |
            | Commit          |
        And I should see following text in following services
            | service    | text                             |
            | potable    | Jan. 26, 2015, Annual            |
            | potable    | Add Survey                       |
            | fire       | Fire water supply is not present |
            | irrigation | Add Survey                       |
        And I should not see following text in following services
            | service | text       |
            | fire    | Add Survey |


    Scenario: Admin is opening site detail page
        Given I open "login" page
        And I login as "admin"
        When I open "site detail" page with pk "10"
        Then I should see following
            | text            |
            | Gabe Newell     |
            | Assign Surveyor |
            | Assign Tester   |
            | Edit            |
            | Commit          |
        And I should see following text in following services
            | service    | text                             |
            | potable    | Jan. 26, 2015, Annual            |
            | potable    | Add Survey                       |
            | fire       | Fire water supply is not present |
            | irrigation | Add Survey                       |
        And I should not see following text in following services
            | service | text       |
            | fire    | Add Survey |


    Scenario: Surveyor is opening site detail page
        Given I open "login" page
        And I login as "surveyor"
        When I open "site detail" page with pk "10"
        Then I should see following
            | text        |
            | Gabe Newell |
            | Commit      |
        And I should not see following
            | text            |
            | Assign Surveyor |
            | Assign Tester   |
            | Edit Site       |
        And I should see following text in following services
            | service    | text                             |
            | potable    | Jan. 26, 2015, Annual            |
            | fire       | Fire water supply is not present |
            | irrigation | Add Survey                       |
        And I should not see following text in following services
            | service | text       |
            | potable | Add Survey |
            | fire    | Add Survey |


    Scenario: Tester is opening site detail page
        Given I open "login" page
        And I login as "tester"
        When I open "site detail" page with pk "10"
        Then I should see following
            | text        |
            | Gabe Newell |
            | Commit      |
        And I should not see following
            | text            |
            | Assign Surveyor |
            | Assign Tester   |
            | Edit Site       |
        And I should see following text in following services
            | service | text                             |
            | potable | Seattle, Digester                |
            | fire    | Fire water supply is not present |
        And I should not see following text in following services
            | service    | text                  |
            | potable    | Jan. 26, 2015, Annual |
            | potable    | Add Survey            |
            | fire       | Add Survey            |
            | irrigation | Add Survey            |