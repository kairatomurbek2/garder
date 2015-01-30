Feature: Site list


    Scenario: Root is opening site list page
        Given I open "login" page
        When I login as "root"
        Then I should see following
            | text        |
            | First Site  |
            | Second Site |
            | Houston     |
            | Ancoridge   |
            | Seattle     |
            | New York    |

    Scenario: Admin is opening site list page
        Given I open "login" page
        When I login as "admin"
        Then I should see following
            | text      |
            | Ancoridge |
            | Chikago   |
            | Seattle   |
        And I should not see following
            | text        |
            | First Site  |
            | Second Site |
            | Boston      |
            | Houston     |
            | Washington  |

    Scenario: Surveyor is opening site list page
        Given I open "login" page
        When I login as "surveyor"
        Then I should see following
            | text       |
            | First Site |
            | Seattle    |
        And I should not see following
            | text        |
            | Second Site |
            | Boston      |
            | Houston     |
            | Washington  |
            | Ancoridge   |

    Scenario: Tester is opening site list page
        Given I open "login" page
        When I login as "tester"
        Then I should see following
            | text        |
            | Second Site |
            | New York    |
            | Seattle     |
        And I should not see following
            | text       |
            | First Site |
            | Boston     |
            | Houston    |
            | Washington |
            | Ancoridge  |