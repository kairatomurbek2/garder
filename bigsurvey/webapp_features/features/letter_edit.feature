@letter
@letter_edit
Feature: Letter Editing

  Scenario Outline: Letter Edit Page Access
    Given I logged in as "<role>"
    When I directly open "letter_edit" page with pk "<pk>"
    Then I should <reaction> "Page not found"
    And I logout
  Examples:
    | role     | pk | reaction |
    | root     | 1  | not see  |
    | root     | 2  | not see  |
    | admin    | 1  | see      |
    | admin    | 2  | not see  |
    | surveyor | 1  | see      |
    | surveyor | 2  | not see  |
    | tester   | 1  | see      |
    | tester   | 2  | see      |

  Scenario: Correct Letter Editing
    Given I logged in as "root"
    And I open "letter_edit" page with pk "2"
    And I select "Due Install Second" from "letter_type"
    And I submit "letter_generate_form" form
    Then I should be at "letter_detail" page with pk "2"
    And I should see "letter editing success" message
#    And I should see warning letter message
#    And I should see warning due date letter message
    And I should see following
      | text                |
      | Gabe Newell         |
      | Dear Customer       |
      | The City of Seattle |
      | 2-nd Notice         |
      | May 05, 2015        |
      | As mentioned above  |
    And I logout

  Scenario: Incorrect Letter Editing
    Given I logged in as "root"
    And I open "letter_edit" page with pk "1"
    And I select "" from "letter_type"
    And I submit "letter_generate_form" form
    Then I should be at "letter_edit" page for site with pk "1"
    And I should see "letter editing error" message
    And I should see following validation error messages on following fields
      | field       | error_message           |
      | letter_type | This field is required. |
    And I logout