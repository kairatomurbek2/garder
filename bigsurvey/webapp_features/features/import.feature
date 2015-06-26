@import
Feature: Import from Excel files

  Scenario Outline: Import page access
    Given I logged in as "<role>"
    When I directly open "import" page
    Then I should <reaction> "Page not found"
    And I logout

  Examples:
    | role     | reaction |
    | root     | not see  |
    | admin    | not see  |
    | surveyor | see      |
    | tester   | see      |

  Scenario: Correct Import
    Given I logged in as "root"
    When I open "import" page
    And I fill in file input "file" with "correct.xlsx"
    And I select "Houston PWS" from "pws"
    And I submit "import" form
    Then I should be at "import_mappings" page
    When I fill in mappings
    And I submit "import-mappings" form
    Then I should be at "import_mappings" page
    When I wait for 5 seconds
    And I refresh page
    Then I should see following
      | text      |
      | 110000110 |
      | 110000120 |
      | 110000125 |
      | 110000200 |
      | 110000301 |
      | 110000310 |
      | 110000490 |
      | 110000495 |
      | 110000497 |
    When I open "import_log_list" page
    Then Last import should have following data
      | added_sites | updated_sites | deactivated_sites |
      | 9           | 0             | 0                 |
    When I open "import" page
    And I fill in file input "file" with "correct-new.xlsx"
    And I select "Houston PWS" from "pws"
    And I submit "import" form
    And I fill in mappings
    And I submit "import-mappings" form
    And I wait for 5 seconds
    And I open "import_log_list" page
    Then Last import should have following data
      | added_sites | updated_sites | deactivated_sites |
      | 1           | 6             | 3                 |
    And I reset database

  Scenario: Incorrect Import
    Given I logged in as "root"
    When I open "import" page
    And I fill in file input "file" with "correct.xlsx"
    And I select "Houston PWS" from "pws"
    And I submit "import" form
    Then I should be at "import_mappings" page
    And I submit "import-mappings" form
    Then I should be at "import_mappings_process" page
    And I should see "required fields not filled" message

  Scenario Outline: Excel file not correct
    Given I logged in as "root"
    When I open "import" page
    And I fill in file input "file" with "<file>"
    And I select "Houston PWS" from "pws"
    And I submit "import" form
    Then I should be at "import_mappings" page
    When I fill in mappings
    And I submit "import-mappings" form
    Then I should be at "import_mappings_process" page
    And I should see "<message>" message with params "<params>"
    And I logout

  Examples:
    | file                         | message                 | params                                     |
    | incorrect_date_format.xlsx   | incorrect date format   | D6 :: %Y%m%d                               |
    | duplicate_cust_numbers.xlsx  | duplicate cust numbers  | A6 :: A10                                  |
    | foreign_key_error.xlsx       | foreign key error       | C7 :: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 :: 100 |
    | required_value_is_empty.xlsx | required value is empty | A4                                         |