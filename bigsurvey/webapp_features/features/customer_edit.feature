@customer_edit
Feature: Customer editing


  Scenario Outline: Customer editing page access
    Given I logged in as "<role>"
    When I directly open "customer_edit" page with pk "4"
    Then I should <reaction> "Not Found"
    And I logout
  Examples:
    | role     | reaction |
    | root     | not see  |
    | admin    | not see  |
    | surveyor | see      |
    | tester   | see      |


  Scenario: Correct customer editing
    Given I logged in as "root"
    And I open "customer_edit" page with pk "4"
    And I fill in following fields with following values
      | field  | value   |
      | number | QAZ2WSX |
    When I submit "customer" form
    Then I should be at "customer_list" page
    And I should see "customer editing success" message
    And I should see "QAZ2WSX"


  Scenario: Incorrect customer editing
    Given I logged in as "root"
    And I open "customer_edit" page with pk "4"
    And I fill in "number" with ""
    When I submit "customer" form
    Then I should be at "customer_edit" page with pk "4"
    And I should see "customer editing error" message
    And I should see "This field is required." validation error message on field "number"