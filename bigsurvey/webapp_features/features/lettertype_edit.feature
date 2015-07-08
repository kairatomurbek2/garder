@lettertype_edit
Feature: Letter Type editing
@wip
  Scenario Outline: Letter Type Edit Page Access
    Given I logged in as "<role>"
    When I directly open "letter_type_edit" page with pk "<pk>"
    Then I should <reaction> "Page not found"
    And I logout
  Examples:
    | role     | pk | reaction |
    | root     | 1  | not see  |
    | surveyor | 1  | see      |
    | tester   | 1  | see      |

  Scenario: Correct Letter Type Edit
    Given I logged in as "admin"
    And I open "letter_type_edit" page that belongs to "admin"'s PWS
    When I change template to "Hello world"
    And I submit "lettertype" form
    Then Letter that belongs to PWS should contain "Hello world"