@site_add
Feature: Site adding


  Scenario Outline: Site adding page access
    Given I logged in as "<role>"
    When I directly open "site_add" page
    Then I should <reaction> "Page not found"
  Examples:
    | role     | reaction |
    | root     | not see  |
    | admin    | not see  |
    | surveyor | see      |
    | tester   | see      |


  Scenario: Correct site adding
    Given I logged in as "root"
    And I open "site_add" page
    And I fill in following fields with following values
      | field        | value               |
      | connect_date | 2015-01-30          |
      | city         | Moscow              |
      | zip          | 000000              |
      | address1     | Red Square, Cremlin |
      | cust_name    | Putin V. V.         |
      | cust_number  | RUSSIA1             |
    And I select "Houston PWS" from "pws"
    And I select "Idaho" from "state"
    And I select "Agricultural" from "site_use"
    And I select "Grocery Store" from "site_type"
    And I select "2" from "floors"
    And I select "Yard" from "interconnection_point"
    And I select "Other" from "cust_code"
    When I submit "site" form
    And I should see "site adding success" message
    And I should see following
      | text                |
      | Moscow              |
      | Red Square, Cremlin |
      | Putin V. V.         |
      | Agricultural        |
      | Grocery Store       |


  Scenario: Incorrect site adding
    Given I logged in as "root"
    And I open "site_add" page
    And I fill in "connect_date" with "not a valid date"
    When I submit "site" form
    Then I should be at "site_add" page
    And I should see "site adding error" message
    And I should see following validation error messages on following fields
      | field        | error_message           |
      | connect_date | Enter a valid date.     |
      | city         | This field is required. |
      | address1     | This field is required. |
      | cust_number  | This field is required. |
      | cust_code    | This field is required. |
      | cust_name    | This field is required. |