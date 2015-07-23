@site_edit
Feature: Site editing
  @keep_db
  Scenario Outline: Site editing page access
    Given I logged in as "<role>"
    When I directly open "site_edit" page with pk "<pk>"
    Then I should <reaction> "Page not found"
  Examples:
    | role     | pk | reaction |
    | root     | 3  | not see  |
    | root     | 4  | not see  |
    | admin    | 3  | see      |
    | admin    | 4  | not see  |
    | surveyor | 3  | see      |
    | surveyor | 4  | not see  |
    | tester   | 3  | see      |


  Scenario: Correct site editing
    Given I logged in as "root"
    And I open "site_edit" page with pk "4"
    And I fill in following fields with following values
      | field    | value                |
      | address1 | 20/12 Central Square |
    When I submit "site" form
    Then I should be at "site_detail" page with pk "4"
    And I should see "site editing success" message
    And I should see "20/12 Central Square"

  Scenario: Site editing by surveyor
    Given I logged in as "surveyor"
    When I open "site_edit" page with pk "4"
    Then I should see only 3 following fields in "site" form
      | field              |
      | potable_present    |
      | fire_present       |
      | irrigation_present |

  Scenario: Incorrect site editing
    Given I logged in as "root"
    And I open "site_edit" page with pk "4"
    And I fill in "connect_date" with "qaz2wsx"
    When I submit "site" form
    Then I should be at "site_edit" page with pk "4"
    And I should see "site editing error" message
    And I should see "Enter a valid date." validation error message on field "connect_date"