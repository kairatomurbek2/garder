@test_add
Feature: Test adding
  @keep_db
  Scenario Outline: Test adding page access
    Given I logged in as "<role>"
    When I directly open "test_add" page for hazard with pk "<pk>"
    Then I should <reaction> "Page not found"
  Examples:
    | role      | pk | reaction |
    | root      | 1  | not see  |
    | root      | 2  | not see  |
    | admin     | 2  | not see  |
    | admin     | 1  | see      |
    | surveyor  | 1  | see      |
    | surveyor  | 2  | see      |
    | tester    | 2  | not see  |
    | tester    | 1  | not see  |
    | root      | 4  | not see  |
    | admin     | 4  | see      |
    | surveyor  | 4  | see      |
    | tester    | 4  | see      |
    | pws_owner | 1  | not see  |
    | pws_owner | 2  | not see  |
    | pws_owner | 4  | see      |


  Scenario: Correct test adding for RP Hazard
    Given I logged in as "tester"
    And Hazard with pk "2" has "RP" assembly type
    When I directly open "test_add" page for hazard with pk "2"
    And I fill in following fields with following values
      | field              | value  |
      | cv1_gauge_pressure | 123456 |
      | cv2_gauge_pressure | 321    |
    And I select "tester" from "tester"
    And I choose "True" from "test_result"
    And I choose "True" from "cv1_leaked"
    And I choose "False" from "cv2_leaked"
    And I choose "True" from "cv1_cleaned"
    And I choose "True" from "rv_cleaned"
    And I choose "True" from "cv2_cleaned"
    And I choose "True" from "outlet_sov_leaked"
    And I check "rv_did_not_open"
    And I submit "test" form
    Then I should see pay modal
    When I close pay modal
    Then I should be redirected to "unpaid_test_list" page
    And I should see following
      | text   |
      | tester |
      | Passed |
      | VALVE  |

  Scenario: Correct test adding for DC Hazard
    Given I logged in as "tester"
    And Hazard with pk "2" has "DC" assembly type
    When I directly open "test_add" page for hazard with pk "2"
    And I fill in following fields with following values
      | field              | value  |
      | cv1_gauge_pressure | 123456 |
      | cv2_gauge_pressure | 321    |
    And I select "tester" from "tester"
    And I choose "True" from "test_result"
    And I choose "True" from "cv1_cleaned"
    And I choose "True" from "cv2_cleaned"
    And I submit "test" form
    Then I should see pay modal
    When I close pay modal
    Then I should be redirected to "unpaid_test_list" page
    And I should see following
      | text   |
      | tester |
      | Passed |
      | VALVE  |

  Scenario: Correct test adding for PVB Hazard
    Given I logged in as "tester"
    And Hazard with pk "2" has "PVB" assembly type
    When I directly open "test_add" page for hazard with pk "2"
    And I fill in "air_inlet_psi" with "1232"
    And I select "tester" from "tester"
    And I choose "True" from "test_result"
    And I choose "True" from "pvb_cleaned"
    And I check "cv_leaked"
    And I submit "test" form
    Then I should see pay modal
    When I close pay modal
    Then I should be redirected to "unpaid_test_list" page
    And I should see following
      | text   |
      | tester |
      | Passed |
      | VALVE  |