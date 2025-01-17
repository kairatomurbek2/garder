@user
@user_edit
Feature: User editing

  @keep_db
  @user_edit_page_access
  Scenario Outline: User editing page access
    Given I logged in as "<role>"
    When I directly open "user_edit" page with pk "<pk>"
    Then I should <reaction> "Page not found"
  Examples:
    | role      | pk  | reaction |
    | root      | 3   | not see  |
    | root      | 10  | not see  |
    | admin     | 3   | not see  |
    | admin     | 10  | see      |
    | surveyor  | 3   | see      |
    | surveyor  | 10  | see      |
    | tester    | 3   | see      |
    | tester    | 10  | see      |
    | admin     | 12  | see      |
    | pws_owner | 12  | not see  |
    | pws_owner | 2   | not see  |
    | pws_owner | 3   | not see  |
    | pws_owner | 4   | not see  |
    | pws_owner | 1   | see      |
    | pws_owner | 10  | see      |


  Scenario: Correct user editing
    Given I logged in as "root"
    And I open "user_edit" page with pk "3" from tab 4
    And I fill in following fields with following values
      | field      | value             |
      | first_name | New Surveyor Name |
    When I submit "user" form
    Then I should be at "user_list" page
    And I should see "user editing success" message
    And I should see "New Surveyor Name" in tab 4


  Scenario: Incorrect user editing
    Given I logged in as "root"
    And I open "user_edit" page with pk "3" from tab 4
    And I fill in following fields with following values
      | field     | value  |
      | username  | admin  |
      | password1 | 123456 |
    When I submit "user" form
    Then I should be at "user_edit" page with pk "3"
    And I should see "user editing error" message
    And I should see following validation error messages on following fields
      | field     | error_message                           |
      | username  | User with this Username already exists. |
      | password2 | The two password fields didn't match.   |

    @admin_self_edit
    Scenario: Administrator self edit
      Given I logged in as "admin"
      And I open "user_edit" page with pk "4" from tab 1
      When I submit "user" form
      Then I should be at "user_list" page
      And I should see following user in following tab
        | user     | tab |
        | admin    | 1   |
        | surveyor | 2   |
        | tester   | 3   |

    @admin_tester_edit
    # checks that tester is not removed from PWS which admin can not select
    Scenario: Admin edits tester
      Given I logged in as "admin"
      And I open "user_edit" page with pk "2" from tab 3
      And I submit "user" form
      When I open "user_list" page
      Then I should see "PWS3" in tab 3

  Scenario: Superadmin is not allowed to edit other superadmin
    Given I logged in as "superadmin"
    And I open "user_edit" page with pk "1" from tab 1
    Then I should see "Page not found"
