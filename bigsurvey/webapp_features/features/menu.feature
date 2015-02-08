@menu
Feature: Menu


    Scenario: Root Menu
        Given I open "login" page
        When I login as "root"
        Then I should see following menu links
            | link      |
            | admin     |
            | pws       |
            | customers |
            | letters   |
            | import    |
            | sites     |


    Scenario: Admin Menu
        Given I open "login" page
        When I login as "admin"
        Then I should see following menu links
            | link      |
            | customers |
            | letters   |
            | import    |
            | sites     |
        And I should not see following menu links
            | link  |
            | admin |
            | pws   |


    Scenario: Surveyor Menu
        Given I open "login" page
        When I login as "surveyor"
        Then I should see following menu links
            | link  |
            | sites |
        And I should not see following menu links
            | link      |
            | admin     |
            | pws       |
            | customers |
            | letters   |
            | import    |


    Scenario: Tester Menu
        Given I open "login" page
        When I login as "tester"
        Then I should see following menu links
            | link  |
            | sites |
        And I should not see following menu links
            | link      |
            | admin     |
            | pws       |
            | customers |
            | letters   |
            | import    |