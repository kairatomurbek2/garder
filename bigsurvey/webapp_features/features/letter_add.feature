@letter
@letter_add
Feature: Letter Adding

  Scenario Outline: Letter Add Page Access
    Given I logged in as "<role>"
    When I directly open "letter_add" page for site with pk "<pk>"
    Then I should <reaction> "Page not found"
    And I logout
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
    And I open "letter_add" page for site with pk "5"
    And I select "Pool" from "letter_type"
    And I select "Digester" from "hazard"
    And I submit "letter_generate_form" form
    Then I should be at "letter_detail" page with pk "3"
    And I should see "letter adding success" message
    And I should see warning letter message
    And I should see following
    | text                   |
    | my swimming pool       |
    | Dear Customer          |
    | The City of Washington |
    | thesomeq@gmail.com     |
    | Amanda James           |
    | QAZ2WSX                |
    | Washington, DC, 90192  |
    | 2015-05-31             |
    | White House            |
    And I logout
    And letter is deleted

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
    And I logout