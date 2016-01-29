@price_setup
Feature: Price Setup

  @keep_db
  Scenario Outline: Price setup page access
    Given I logged in as "<role>"
    When I directly open "price_setup" page
    Then I should <reaction> "Page not found"

  Examples:
    | role       | reaction |
    | root       | not see  |
    | superadmin | not see  |
    | pws_owner  | see      |
    | admin      | see      |
    | surveyor   | see      |
    | tester     | see      |


  Scenario Outline: Price incorrect editing
    Given I logged in as "root"
    And I open "price_setup" page
    When I fill in "price" with "<value>"
    And I submit "price_setup" form
    Then I should see "<error_message>"

  Examples:
    | value | error_message                                      |
    | 1     | New Price can not be the same as the current Price |
    | -1    | Price per Test can not be lower than 0             |


  Scenario: Price adding
    Given I logged in as "root"
    And I directly open "price_setup" page
    When I fill in "price" with "2"
    And I submit "price_setup" form
    Then I should see following
      | text |
      | 2.00 |
      | 1.00 |


  Scenario: Price updating
    Given Current default price started today
    And I logged in as "root"
    And I directly open "price_setup" page
    When I fill in "price" with "2"
    And I submit "price_setup" form
    Then I should see "2.00"
    And I should not see "1.00"