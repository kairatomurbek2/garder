@lettertype_edit
Feature: Letter Type editing

  Scenario Outline: Letter Type Edit Page Access
    Given I logged in as "<role>"
    When I directly open "letter_type_edit" page with pk "<pk>"
    Then I should <reaction> "Page not found"
    And I logout
    Examples:
      | role     | pk | reaction |
      | root     | 31 | not see  |
      | root     | 37 | not see  |
      | admin    | 31 | not see  |
      | admin    | 37 | see      |
      | surveyor | 31 | see      |
      | surveyor | 37 | see      |
      | tester   | 31 | see      |
      | tester   | 37 | see      |

  Scenario: Correct Letter Type Edit
    Given I logged in as "admin"
    And I open "letter_type_edit" page with pk "31"
    When I change template to "Hello world"
    And I submit "lettertype" form
    Then Letter type template with pk "31" should contain "Hello world"