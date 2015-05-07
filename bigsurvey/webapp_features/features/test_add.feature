@test_add
Feature: Test adding
  Scenario: Empty Scenario For Test Purposes
    When I logged in as "root"
    Then I logout
#
#
#  Scenario Outline: Test adding page access
#    Given I logged in as "<role>"
#    When I directly open "test_add" page for hazard with pk "<pk>"
#    Then I should <reaction> "Not Found"
#    And I logout
#  Examples:
#    | role     | pk | reaction |
#    | root     | 1  | not see  |
#    | root     | 2  | not see  |
#    | admin    | 2  | not see  |
#    | admin    | 1  | see      |
#    | surveyor | 1  | see      |
#    | surveyor | 2  | see      |
#    | tester   | 2  | not see  |
#    | tester   | 1  | see      |
#
#
#  Scenario: Correct test adding
#    Given I logged in as "root"
#    And I open "test_add" page for hazard with pk "2"
#    And I fill in following fields with following values
#      | field                 | value      |
#      | cv1_gauge_pressure    | 123456     |
#    And I select "tester" from "tester"
#    When I submit "test" form
#    Then I should be at "hazard_detail" page with pk "2"
#    And I should see "test adding success" message
#    And I should see following
#      | text    |
#      | tester  |
#      | 123456  |