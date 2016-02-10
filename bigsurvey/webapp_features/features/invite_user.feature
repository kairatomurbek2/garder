@invite_user
Feature: User Invite

  @keep_db
  Scenario Outline: User Invite Page Access
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
  Scenario: Search for existing user
    Given I logged in as "admin"
    And I open "invite" page
    When I select "Testers" from "group"
    And I fill in "email" with "nopws@tester.com"
    And I submit "search_user" form
    Then I should be at "invite" page
    And I should see following
      | text          |
      | tester_no_pws |
      | NUI812        |
      | Invite        |

  @keep_db
  Scenario: Search for non-tester
    Given I logged in as "admin"
    And I open "invite" page
    When I select "Surveyors" from "group"
    And I fill in "username" with "surveyor"
    And I submit "search_user" form
    Then I should be at "invite" page
    And I should see following
     | text          |
     | surveyor city |
     | NUI812        |
     | Invite        |

  @keep_db
  Scenario: Search for already employed user
    Given I logged in as "admin"
    And I open "invite" page
    And I select "Testers" from "group"
    And I fill in "username" with "tester"
    And I fill in "cert_number" with "qwerty132"
    And I submit "search_user" form
    And I should be at "invite" page
    When I select "NUI812" from "pws"
    And I select "tester" from "user"
    And I click "invite_user" button
    Then I should be at "invite" page
    And I should see "Selected user is employee of selected PWS already"

  @keep_db
  Scenario: Search for unexisting tester
    Given I logged in as "admin"
    And I open "invite" page
    When I select "Administrators" from "group"
    And I fill in "username" with "vasya"
    And I submit "search_user" form
    Then I should be at "invite" page
    And I should see following
      | text                                   |
      | User with such personal data not found |
    And I should not see "Invite"

  @keep_db
  Scenario: Search for without criteria
    Given I logged in as "admin"
    And I open "invite" page
    When I select "Testers" from "group"
    And I submit "search_user" form
    Then I should be at "invite" page
    And I should see following
      | text                                 |
      | Either username or email is required |
    And I should not see "Invite"
