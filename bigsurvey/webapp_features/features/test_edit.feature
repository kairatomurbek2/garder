@test_edit
Feature: Test editing
  @keep_db
  Scenario Outline: Test editing page access
    Given I logged in as "<role>"
    When I directly open "test_edit" page with pk "<pk>"
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

  Scenario: Correct test editing
    Given I logged in as "root"
    And Hazard with pk "2" has "RP" assembly type
    When I open "test_edit" page with pk "2"
    And I fill in following fields with following values
      | field              | value  |
      | cv2_gauge_pressure | 111111 |
    And I submit "test" form
    Then I should be at "test_detail" page with pk "2"
    And I should see "test editing success" message
    And I should see "111111"

  Scenario: Check test_date is editable
    Given I logged in as "tester"
    And I directly open "test_edit" page with pk "3"
    And I fill in "test_date" with "2015-07-08"
    When I submit "test" form
    Then I should be at "test_detail" page with pk "3"
    And I should see following
      | text         |
      | July 8, 2015 |