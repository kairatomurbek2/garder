@customer_add
Feature: Customer adding


  Scenario Outline: Customer adding page access
    Given I logged in as "<role>"
    When I directly open "customer_add" page
    Then I should <reaction> "Not Found"
    And I logout
  Examples:
    | role     | reaction |
    | root     | not see  |
    | admin    | not see  |
    | surveyor | see      |
    | tester   | see      |


  Scenario: Correct customer adding
    Given I logged in as "root"
    And I open "customer_add" page
    And I fill in following fields with following values
      | field    | value         |
      | number   | CUST987       |
      | name     | Ivan Ivanov   |
      | city     | Bishkek       |
      | zip      | 123456789     |
      | address1 | Hello, world! |
    And I select "Fire" from "code"
    And I select "Kansas" from "state"
    When I submit "customer" form
    Then I should be at "customer_list" page
    And I should see "customer adding success" message
    And I should see following
      | text          |
      | CUST987       |
      | Ivan Ivanov   |
      | Bishkek       |
      | Hello, world! |


  Scenario: Incorrect customer adding
    Given I logged in as "root"
    And I open "customer_add" page
    When I submit "customer" form
    Then I should be at "customer_add" page
    And I should see "customer adding error" message
    And I should see following validation error messages on following fields
      | field    | error_message           |
      | number   | This field is required. |
      | name     | This field is required. |
      | code     | This field is required. |
      | city     | This field is required. |
      | address1 | This field is required. |