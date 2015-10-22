@invite_tester
Feature: Tester Invite

  @keep_db
  Scenario Outline: Tester Invite Page Access
    Given I logged in as "<role>"
    When I directly open "invite" page
    Then I should <reaction> "Page not found"

    Examples:
     | role      | reaction |
     | root      | not see  |
     | admin     | not see  |
     | pws_owner | not see  |
     | tester    | see      |
     | surveyor  | see      |

  @keep_db
  Scenario: Search for existing tester
    Given I logged in as "admin"
    And I open "invite" page
    When I fill in "email" with "nopws@tester.com"
    And I submit "search_tester" form
    Then I should be at "invite" page
    And I should see following
      | text          |
      | tester_no_pws |
      | NUI812        |
      | Invite        |

  @keep_db
  Scenario: Search for already employed tester
    Given I logged in as "admin"
    And I open "invite" page
    When I fill in "email" with "tester@example.com"
    And I fill in "cert_number" with "qwerty132"
    And I submit "search_tester" form
    Then I should be at "invite" page
    And I should see following
      | text                                            |
      | tester                                          |
      | Selected tester is employee of your PWS already |
    And I should not see following
      | Invite |

  @keep_db
  Scenario: Search for unexisting tester
    Given I logged in as "admin"
    And I open "invite" page
    When I fill in "email" with "nosuch@e.mail"
    And I submit "search_tester" form
    Then I should be at "invite" page
    And I should see following
      | text                                                    |
      | Tester with such email and certificate number not found |
    And I should not see following
      | Invite |