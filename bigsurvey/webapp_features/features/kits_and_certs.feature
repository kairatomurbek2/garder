@kits_and_certs
Feature: Test Kits and Certificates

  @keep_db
  Scenario Outline: Test Kit and Certificates pages access
    Given I logged in as "<role>"
    When I directly open "<page>" page with pk <pk>
    Then I should <reaction> "Page not found"

    Examples:
      | role      | page      | pk | reaction |
      | root      | kit_add   | 2  | not see  |
      | pws_owner | kit_add   | 2  | not see  |
      | admin     | kit_add   | 2  | not see  |
      | surveyor  | kit_add   | 2  | see      |
      | tester    | kit_add   | 2  | see      |
      | root      | kit_edit  | 1  | not see  |
      | pws_owner | kit_edit  | 1  | not see  |
      | admin     | kit_edit  | 1  | not see  |
      | surveyor  | kit_edit  | 1  | see      |
      | tester    | kit_edit  | 1  | see      |
      | root      | cert_add  | 2  | not see  |
      | pws_owner | cert_add  | 2  | not see  |
      | admin     | cert_add  | 2  | not see  |
      | surveyor  | cert_add  | 2  | see      |
      | tester    | cert_add  | 2  | see      |
      | root      | cert_edit | 1  | not see  |
      | pws_owner | cert_edit | 1  | not see  |
      | admin     | cert_edit | 1  | not see  |
      | surveyor  | cert_edit | 1  | see      |
      | tester    | cert_edit | 1  | see      |

  @kc_form_steps
  Scenario: Correct Kit adding
    Given I logged in as "root"
    And I open "kit_add" page with pk 9
    And I fill in "test_serial" with "serial123"
    When I submit "test_kit" form
    Then I should be at "user_detail" page with pk 9
    And I should see "serial123"
    And I should not see "No Test Kits Available."

  @kc_form_steps
  Scenario: Correct Kit editing
    Given I logged in as "root"
    And I open "kit_edit" page with pk 1
    And I fill in "test_serial" with "number2"
    When I submit "test_kit" form
    Then I should be at "user_detail" page with pk 2
    And I should see "number2"
    And I should not see "number1"

  @kc_form_steps
  Scenario: Correct Cert adding
    Given I logged in as "root"
    And I open "cert_add" page with pk 9
    And I fill in "cert_number" with "number123"
    When I submit "tester_cert" form
    Then I should be at "user_detail" page with pk 9
    And I should see "number123"
    And I should not see "No Certificates Available."

  @kc_form_steps
  Scenario: Correct Cert editing
    Given I logged in as "root"
    And I open "cert_edit" page with pk 1
    And I fill in "cert_number" with "qwerty213"
    When I submit "tester_cert" form
    Then I should be at "user_detail" page with pk 2
    And I should see "qwerty213"
    And I should not see "qwerty132"


  Scenario Outline: Test Kit and Certificates pages access for user
    Given I logged in as "<role>"
    When I directly open "<page>" page with pk <pk>
    Then I should <reaction> "Page not found"
    Examples:
      | role  | page     | pk | reaction |
      | admin | kit_add  | 4  | see      |
      | admin | kit_add  | 3  | see      |
      | admin | kit_add  | 2  | not see  |
      | admin | cert_add | 4  | see      |
      | admin | cert_add | 3  | see      |
      | admin | cert_add | 2  | not see  |
