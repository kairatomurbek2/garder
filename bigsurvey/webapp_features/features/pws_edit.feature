@pws_edit
Feature: PWS editing

  Scenario Outline: PWS editing page access
    Given I logged in as "<role>"
    When I directly open "pws_edit" page with pk "6"
    Then I should <reaction> "Page not found"
  Examples:
    | role     | reaction |
    | root     | not see  |
    | admin    | see      |
    | surveyor | see      |
    | tester   | see      |

  Scenario: Correct PWS editing
    Given I logged in as "root"
    And I open "pws_edit" page with pk "6"
    And I fill in "notes" with "This is notes for PWS with id=6"
    And I fill in file input "logo" with "logo.jpg"
    When I submit "pws" form
    Then I should be at "pws_detail" page with pk "6"
    And I should see "pws editing success" message
    And I should see "This is notes for PWS with id=6"
    And "logo.jpg" should be uploaded
    When I open "pws_edit" page with pk "6"
    And I check "logo-clear"
    And I submit "pws" form
    Then "logo.jpg" should be deleted

  Scenario: Correct PWS editing as admin
    Given I logged in as "admin"
    And I directly open "pws_edit" page with pk "9"
    When I fill in following fields with following values
      | field            | value       |
      | consultant_phone | +19265429   |
      | city             | Minneapolis |
    And I submit "pws" form
    Then I should be at "pws_detail" page with pk "9"
    And I should see "pws editing success" message
    And PWS with pk "9" should contain "+19265429" in "consultant_phone" field
    And PWS with pk "9" should contain "Minneapolis" in "city" field

  Scenario: Incorrect PWS editing
    Given I logged in as "root"
    And I open "pws_edit" page with pk "6"
    And I fill in "name" with ""
    When I submit "pws" form
    Then I should be at "pws_edit" page with pk "6"
    And I should see "pws editing error" message
    And I should see "This field is required." validation error message on field "name"
