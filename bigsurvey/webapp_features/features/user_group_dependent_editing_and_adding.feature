@user
@user_add
@user_edit

Feature: User adding and editing depending on the user's group

  Scenario: Adding users by PWS owner
    Given I logged in as pws owner
    When I open user adding form
    Then I see the following user groups to choose from:
      | group          |
      | Administrators |
      | Surveyors      |
      | Testers        |

  Scenario Outline: Editing users by PWS owner
    Given I logged in as pws owner
    When I open editing form of "<user>" from usergroup "<group>"
    Then I see the following user groups to choose from:
      | group          |
      | Administrators |
      | Surveyors      |
      | Testers        |
    Examples:
      | user     | group          |
      | owner    | PWS Owners     |
      | admin    | Administrators |
      | surveyor | Surveyors      |
      | tester   | Testers        |

  Scenario: Adding users by pws admin
    Given I logged in as pws admin
    When I open user adding form
    Then I see the following user groups to choose from:
      | group          |
      | Surveyors      |
      | Testers        |

  Scenario Outline: Editing users by pws admin
    Given I logged in as pws admin
    When I open editing form of "<user>" from usergroup "<group>"
    Then I see the following user groups to choose from:
      | group          |
      | Surveyors      |
      | Testers        |
    Examples:
      | user     | group          |
      | surveyor | Surveyors      |
      | tester   | Testers        |

  Scenario: Admin cannot edit other admins
    Given I logged in as pws admin
    And There is another_admin user in Adminstrators group
    When I open Administrators tab on users page
    Then I do not see action links against user "another_admin" with email "another_admin@admin.admin"
    But I see action links against user "admin" with email "admin@admin.admin"