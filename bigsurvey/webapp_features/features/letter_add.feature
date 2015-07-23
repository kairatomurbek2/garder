@letter
@letter_add
Feature: Letter Adding

  Scenario Outline: Letter Add Page Access
    Given I logged in as "<role>"
    When I directly open "letter_add" page for site with pk "<pk>"
    Then I should <reaction> "Page not found"
  Examples:
    | role     | pk | reaction |
    | root     | 5  | not see  |
    | root     | 10 | not see  |
    | admin    | 5  | see      |
    | admin    | 10 | not see  |
    | surveyor | 5  | see      |
    | surveyor | 10 | not see  |
    | tester   | 5  | see      |
    | tester   | 10 | see      |

  Scenario: Correct Letter Adding
    Given I logged in as "root"
    And PWS with pk "6" has uploaded logo
    When I open "letter_add" page for site with pk "5"
    And I select "Pool" from "letter_type"
    And I select "Digester" from "hazard"
    And I submit "letter_generate_form" form
    Then I should be at "letter_detail" page with pk "3"
    And I should see "letter adding success" message
    And I should see warning letter message
    And I should see following
      | text                   |
      | Dear Customer          |
      | The City of Washington |
      | Amanda James           |
      | QAZ2WSX                |
      | Washington, DC, 90192  |
      | 05/31/2015             |
      | White House            |
    And There should be logo of PWS with pk "6"

  @incorrect_letter_adding
  Scenario: Incorrect Letter Adding
    Given I logged in as "root"
    And I open "letter_add" page for site with pk "7"
    And I submit "letter_generate_form" form
    Then I should be at "letter_add" page for site with pk "7"
    And I should see "letter adding error" message
    And I should see following validation error messages on following fields
      | field       | error_message           |
      | letter_type | This field is required. |
      | hazard      | This field is required. |