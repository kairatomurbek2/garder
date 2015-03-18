@site_filter
Feature: Filtration


  Scenario: Filtration by city field while logged in as root
    Given I logged in as "root"
    And I open "site_list" page
    When I fill in "city" with "on"
    And I submit "site_filter" form
    Then I should see following
      | text        |
      | Second Site |
      | Houston     |
      | Boston      |
      | Washington  |
    And I should not see following
      | text       |
      | First Site |
      | Ancoridge  |
      | New York   |
      | IKW182     |
      | Chikago    |
      | Seattle    |


  Scenario: Filtration by address1 field while logged in as root
    Given I logged in as "root"
    And I open "site_list" page
    When I fill in "address" with "cent"
    And I submit "site_filter" form
    Then I should see following
      | text      |
      | Ancoridge |
    And I should not see following
      | text       |
      | Boston     |
      | Washington |
      | New York   |


  Scenario: Filtration by site_use field while logged in as admin
    Given I logged in as "admin"
    And I open "site_list" page
    When I select "Industrial" from "site_use"
    And I submit "site_filter" form
    Then I should see following
      | text    |
      | Chikago |
    And I should not see following
      | text        |
      | Houston     |
      | Boston      |
      | Washington  |
      | New York    |
      | Los Angeles |


  Scenario: Filtration by site_type field while logged in as tester
    Given I logged in as "tester"
    And I open "site_list" page
    When I select "Governmental" from "site_type"
    And I submit "site_filter" form
    Then I should see following
      | text     |
      | New York |
    And I should not see following
      | text    |
      | Seattle |


  Scenario: Filtration by city and customer fields while logged in as root
    Given I logged in as "root"
    And I open "site_list" page
    When I fill in following fields with following values
      | field    | value  |
      | city     | new    |
      | customer | amanda |
    And I submit "site_filter" form
    Then I should see following
      | text      |
      | Manhattan |
    And I should not see following
      | text       |
      | Washington |


  Scenario: Filtration by site use and type while logged in as root
    Given I logged in as "root"
    And I open "site_list" page
    When I select "Commercial" from "site_use"
    And I select "Offices" from "site_type"
    And I submit "site_filter" form
    Then I should see following
      | text  |
      | VALVE |
    And I should not see following
      | text   |
      | IKW182 |


  Scenario: Filtration by next survey date while logged in as admin
    Given I logged in as "admin"
    And I open "site_list" page
    When I select "Next Year" from "next_survey_date"
    And I submit "site_filter" form
    Then I should see following
      | text    |
      | Chikago |
    And I should not see following
      | text    |
      | Seattle |


  Scenario: Filtration by last survey date while logged in as root
    Given I logged in as "root"
    And I open "site_list" page
    When I select "1 week" from "last_survey_date"
    And I submit "site_filter" form
    Then I should see following
      | text       |
      | Washington |
      | Seattle    |
    And I should not see following
      | text    |
      | Chikago |
      | Boston  |