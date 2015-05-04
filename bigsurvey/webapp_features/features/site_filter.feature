@site_filter
Feature: Filtration


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

  Scenario: Filtration by seq route
    Given I logged in as "root"
    And I open "site_list" page
    When I fill in "route" with "ROUTE-123"
    And I submit "site_filter" form
    Then I should see following
      | text       |
      | Seattle    |
      | Washington |