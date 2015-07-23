@batch_update
Feature: Batch Update

  @keep_db
  Scenario Outline: Batch Update page access
    Given I logged in as "<role>"
    When I directly open "batch_update" page
    Then I should <reaction> "Page not found"

  Examples:
    | role     | reaction |
    | root     | not see  |
    | admin    | not see  |
    | surveyor | see      |
    | tester   | see      |

  Scenario: Correct Batch Updating Sites' Next Survey Date
    Given I logged in as "root"
    And I open "batch_update" page
    And I check following values from "site_pks"
      | value |
      | 8     |
      | 7     |
    And I fill in "date" with "2017-02-10"
    When I click "set_sites_next_survey_date" button
    Then I should see "batch updating success" message
    When I open "site_detail" page with pk "7"
    Then I should see "Feb. 10, 2017"
    When I open "site_detail" page with pk "8"
    Then I should see "Feb. 10, 2017"

  Scenario: Correct Batch Update Hazards' Due Install Test Date
    Given I logged in as "root"
    And I open "batch_update" page
    And I check following values from "site_pks"
      | value |
      | 10    |
    And I fill in "date" with "2015-08-22"
    When I click "set_hazards_due_install_test_date" button
    Then I should see "batch updating success" message
    When I open "hazard_detail" page with pk "2"
    Then I should see "Aug. 22, 2015"

  Scenario: Incorrect Batch Updating
    Given I logged in as "root"
    And I open "batch_update" page
    And I check following values from "site_pks"
      | value |
      | 8     |
      | 7     |
    When I submit "batch_update" form
    Then I should see "batch updating error" message