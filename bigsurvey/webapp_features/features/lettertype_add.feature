@lettertype_add
Feature: Letter Type adding

  Scenario: Correct Letter Type adding
    Given I logged in as "root"
    And I directly open "letter_type_add" page
    And I fill in following fields with following values
      | field       | value            |
      | letter_type | Test Letter Type |
    And I submit form with id "lettertype_form"
    And Letter type with name "Test Letter Type" was cloned to all PWS