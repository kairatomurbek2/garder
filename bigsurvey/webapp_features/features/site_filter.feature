@site_filter
Feature: Filtration

  @keep_db
  @char_filters
  Scenario Outline: Site Filtering by char filters
    Given I logged in as "root"
    And I open "site_list" page
    When I fill in "<filter>" with "<value>"
    And I submit "site_filter" form
    Then I should see sites with ids "<site_ids>"
    And I should not see sites with ids "<other_site_ids>"

    Examples:
      | filter            | value      | site_ids  | other_site_ids     |
      | cust_number       | ZXC2       | 3         | 1,2,4,5,6,7,8,9,10 |
      | cust_name         | Newell     | 10        | 1,2,3,4,5,6,7,8,9  |
      | street_number     | 7269       | 10        | 1,2,3,4,5,6,7,8,9  |
      | address1          | Avenue     | 3,7       | 1,2,4,5,6,8,9,10   |
      | address2          | nowhere    | 3         | 1,2,4,5,6,7,8,9,10 |
      | apt               | 75         | 10        | 1,2,3,4,5,6,7,8,9  |
      | city              | washington | 5         | 1,2,3,4,6,7,8,9,10 |
      | zip               | 12         | 4,6,7     | 1,2,3,5,8,9,10     |
      | cust_address1     | First      | 2         | 1,3,4,5,6,7,8,9,10 |
      | cust_address2     | Beach      | 7         | 1,2,3,4,5,6,8,9,10 |
      | cust_apt          | -          | 10        | 1,2,3,4,5,6,7,8,9  |
      | cust_city         | ashington  | 5,6       | 1,2,3,4,7,8,9,10   |
      | cust_zip          | 0          | 3,4,5,6,9 | 1,2,7,8,10         |
      | route             | 123        | 5,10      | 1,2,3,4,6,7,8,9    |
      | meter_number      | TM         | 8         | 1,2,3,4,5,6,7,9,10 |
      | meter_size        | "          | 9         | 1,2,3,4,5,6,7,8,10 |
      | meter_reading     | 100        | 8         | 1,2,3,4,5,6,7,9,10 |
      | due_test_from     | 2015-05-31 | 5         | 1,2,3,4,6,7,8,9,10 |
      | due_test_to       | 2015-05-31 | 5         | 1,2,3,4,6,7,8,9,10 |
      | next_survey_from  | 2016-02-09 | 9         | 1,2,3,4,5,6,7,8,10 |
      | next_survey_to    | 2015-01-15 | 1         | 2,3,4,5,6,7,8,9,10 |
      | last_survey_from  | 2015-01-26 | 10        | 1,2,3,4,5,6,7,8,9  |
      | last_survey_to    | 2015-01-25 | 5         | 1,2,3,4,6,7,8,9,10 |
      | connect_date_from | 2015-01-22 | 3,4,5,7   | 1,2,6,8,9,10       |
      | connect_date_to   | 2015-01-15 | 1,2       | 3,4,5,6,7,8,9,10   |

  @keep_db
  @list_filters
  Scenario Outline: Site Filtering by list filters
    Given I logged in as "root"
    And I open "site_list" page
    When I select "<value>" from "<filter>"
    And I submit "site_filter" form
    Then I should see sites with ids "<site_ids>"
    And I should not see sites with ids "<other_site_ids>"

    Examples:
      | filter     | value      | site_ids | other_site_ids     |
      | pws        | NUI812     | 4,9,10   | 1,2,3,5,6,7,8      |
      | cust_code  | Industrial | 4,8      | 1,2,3,5,6,7,9,10   |
      | state      | WA         | 10       | 1,2,3,4,5,6,7,8,9  |
      | state      | blank      | 1        | 2,3,4,5,6,7,8,9,10 |
      | cust_state | TX         | 3        | 1,2,4,5,6,7,8,9,10 |
      | cust_state | blank      | 1        | 2,3,4,5,6,7,8,9,10 |

  @keep_db
  @blank_filters
  Scenario Outline: Site Filtering by blank char filters
    Given I logged in as "root"
    And I open "site_list" page
    When I check "<filter>"
    And I submit "site_filter" form
    Then I should see sites with ids "<site_ids>"
    And I should not see sites with ids "<other_site_ids>"

    Examples:
      | filter              | other_site_ids     | site_ids           |
      | street_number_blank | 10                 | 1,2,3,4,5,6,7,8,9  |
      | address2_blank      | 3                  | 1,2,4,5,6,7,8,9,10 |
      | apt_blank           | 10                 | 1,2,3,4,5,6,7,8,9  |
      | zip_blank           | 2,3,4,5,6,7,8,9,10 | 1                  |
      | cust_address1_blank | 2,3,4,5,6,7,8,9,10 | 1                  |
      | cust_address2_blank | 7                  | 1,2,3,4,5,6,8,9,10 |
      | cust_apt_blank      | 10                 | 1,2,3,4,5,6,7,8,9  |
      | cust_city_blank     | 2,3,4,5,6,7,8,9,10 | 1                  |
      | cust_zip_blank      | 2,3,4,5,6,7,8,9,10 | 1                  |
      | route_blank         | 5,10               | 1,2,3,4,6,7,8,9    |
      | meter_number_blank  | 8                  | 1,2,3,4,5,6,7,10   |
      | meter_size_blank    | 9                  | 1,2,3,4,5,6,7,8,10 |
      | meter_reading_blank | 8,9                | 1,2,3,4,5,6,7      |
      | connect_date_blank  | 1,2,3,4,5,7        | 6,8,9,10           |
      | next_survey_blank   | 1,9                | 2,3,4,5,6,7,8,10   |
      | last_survey_blank   | 5,10               | 1,2,3,4,6,7,8,9    |
      | due_test_blank      | 5                  | 1,2,3,4,6,7,8,9,10 |
