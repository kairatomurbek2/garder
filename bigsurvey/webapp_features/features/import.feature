@import
Feature: Import from Excel files

  @keep_db
  Scenario Outline: Import page access
    Given I logged in as "<role>"
    When I directly open "import" page
    Then I should <reaction> "Page not found"

    Examples:
      | role      | reaction |
      | root      | not see  |
      | admin     | not see  |
      | pws_owner | not see  |
      | surveyor  | see      |
      | tester    | see      |

  @import_correct
  Scenario: Correct Import
    Given I logged in as "root"
    And I open "import" page
    And I fill in file input "file" with "correct.xlsx"
    And I select "South Western PWS" from "pws"
    And I select "other" from "date_format"
    And I fill in "date_format_other" with "%Y%m%d"

    When I submit "import" form
    Then I should be at "import_mappings" page

    When I fill in mappings
    And I submit "import-mappings" form
    Then I should be at "import_mappings" page

    When I wait for 10 seconds
    Then I should be at "import_log_list" page
    And Last import should have following data
      | added_sites | updated_sites | deactivated_sites |
      | 9           | 0             | 0                 |
    And I open "home" page
    And I should see following
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

    When I open "import" page
    And I fill in file input "file" with "correct-new.xlsx"
    And I select "South Western PWS" from "pws"
    And I select "other" from "date_format"
    And I fill in "date_format_other" with "%Y%m%d"
    And I submit "import" form
    And I fill in mappings
    And I submit "import-mappings" form
    And I wait for 10 seconds
    Then I should be at "import_log_list" page
    And Last import should have following data
      | added_sites | updated_sites | deactivated_sites |
      | 1           | 6             | 3                 |

  @import_incorrect
  Scenario: Incorrect Import
    Given I logged in as "root"
    When I open "import" page
    And I fill in file input "file" with "correct.xlsx"
    And I select "South Western PWS" from "pws"
    And I select "other" from "date_format"
    And I fill in "date_format_other" with "%Y%m%d"
    And I submit "import" form
    Then I should be at "import_mappings" page
    And I select "----------" from "form-1-excel_field"
    And I submit "import-mappings" form
    Then I should be at "import_mappings_process" page
    And I should see "required fields not filled" message

  @import_file_incorrect
  Scenario Outline: Excel file not correct
    Given I logged in as "root"
    When I open "import" page
    And I fill in file input "file" with "<file>"
    And I select "South Western PWS" from "pws"
    And I select "other" from "date_format"
    And I fill in "date_format_other" with "%Y%m%d"
    And I submit "import" form
    And I fill in mappings
    And I submit "import-mappings" form
    Then I should be at "import_mappings_process" page
    And I should see "<message>" message with params "<params>"

    Examples:
      | file                         | message                 | params                                                                                                                     |
      | incorrect_date_format.xlsx   | incorrect date format   | D6 :: %Y%m%d                                                                                                               |
      | foreign_key_error.xlsx       | foreign key error       | C7 :: Residental, Governmental, Commercial, Industrial, Trailer Park, Multifamily, Irrigation, Fire, Other, Potable :: 100 |
      | required_value_is_empty.xlsx | required value is empty | A4                                                                                                                         |

  @import_duplicates
  Scenario: Import file contains duplicates
    Given I logged in as "root"
    And I open "import" page
    And I fill in file input "file" with "duplicates.xlsx"
    And I select "South Western PWS" from "pws"
    And I select "other" from "date_format"
    And I fill in "date_format_other" with "%Y%m%d"
    And I submit "import" form
    When I submit "import-mappings" form
    And I wait for 10 seconds
    Then I should be at "import_log_list" page
    And Last import should have following data
      | added_sites | updated_sites | deactivated_sites |
      | 9           | 0             | 0                 |
    And I should see warning message with text "Import was finished but 4 duplicate accounts were not imported."
    And Last import should have duplicates file attached

  @import_only_update
  Scenario: Importing without deactivation
    Given I logged in as "root"
    And I open "import" page
    And I fill in file input "file" with "duplicates_fixed.xlsx"
    And I select "White House PWS" from "pws"
    And I select "other" from "date_format"
    And I fill in "date_format_other" with "%Y%m%d"
    And I check "update_only"
    And I submit "import" form
    When I submit "import-mappings" form
    And I wait for 10 seconds
    Then I should be at "import_log_list" page
    And Last import should have following data
      | added_sites | updated_sites | deactivated_sites |
      | 4           | 0             | 0                 |
    And I open "home" page
    And I should see following
      | text      |
      | QAZ2WSX2  |
      | QAZ2WSX   |
      | 110000200 |
      | 110000301 |
    And I should see text "110000301" 3 times
