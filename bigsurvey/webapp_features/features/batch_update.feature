@batch_update
@wip
Feature: Batch Update

  @keep_db
  Scenario Outline: Batch Update page access
    Given I logged in as "<role>"
    When I directly open "batch_update" page
    Then I should <reaction> "Page not found"

  Examples:
    | role      | reaction |
    | root      | not see  |
    | admin     | not see  |
    | pws_owner | not see  |
    | surveyor  | see      |
    | tester    | see      |

  Scenario: Correct Batch Updating Next Survey Date
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

  Scenario: Correct Batch Update Due Install Test Date
    Given I logged in as "root"
    And I open "batch_update" page
    And I check following values from "site_pks"
      | value |
      | 10    |
    And I fill in "date" with "2015-08-22"
    When I click "set_hazards_due_install_test_date" button
    Then I should see "batch updating success" message
    And I should see "Aug. 22, 2015"

  Scenario: Incorrect Batch Updating
    Given I logged in as "root"
    And I open "batch_update" page
    And I check following values from "site_pks"
      | value |
      | 8     |
      | 7     |
    When I submit "batch_update" form
    Then I should see "batch updating error" message

  @batch_update_empty_date
  Scenario: Batch Updating Sites' Next Survey Date with empty date
    Given I logged in as "root"
    And I open "batch_update" page
    And I should see "Jan. 15, 2015"
    And I check following values from "site_pks"
      | value |
      | 1     |
    And I check "empty_date"
    When I click "set_sites_next_survey_date" button
    Then I should see "batch updating success" message
    And I should not see "Jan. 15, 2015"


  @batch_update_empty_date
  Scenario: Batch Updating due test date with empty date
    Given I logged in as "root"
    And I open "batch_update" page
    And I should see "May 31, 2015"
    And I check following values from "site_pks"
      | value |
      | 5     |
    And I check "empty_date"
    When I click "set_hazards_due_install_test_date" button
    Then I should see "batch updating success" message
    And I should not see "May 31, 2015"

  Scenario: Batch Updating create letters
    Given There Hazard letters
    And I logged in as "root"
    And I open "batch_update" page
    And I check following values from "site_pks"
      | value |
      | 11    |
    And I fill in "date" with "2017-02-10"
    When I click "create_letters" button
    Then I should see "letter creation success" message
    And I should see "letters not created for hazards warning" message

