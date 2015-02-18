@site_detail
Feature: Site detail


  Scenario Outline: Site detail page access
    Given I logged in as "<role>"
    When I open "site detail" page with pk "<pk>"
    Then I should <reaction> "Not Found"
    And I logout
  Examples:
    | role     | pk | reaction |
    | root     | 3  | not see  |
    | root     | 4  | not see  |
    | admin    | 3  | see      |
    | admin    | 4  | not see  |
    | surveyor | 3  | see      |
    | surveyor | 2  | not see  |
    | tester   | 3  | see      |
    | tester   | 6  | not see  |


  Scenario: Root is opening site detail page
    Given I logged in as "root"
    When I open "site detail" page with pk "10"
    Then I should see following
      | text        |
      | Gabe Newell |
      | Assign      |
      | Edit        |
      | Commit      |
    And I should see following text in following services
      | service    | text                             |
      | potable    | Jan. 26, 2015                    |
      | potable    | Add Survey                       |
      | fire       | Fire water supply is not present |
      | irrigation | Add Survey                       |
    And I should not see following text in following services
      | service | text       |
      | fire    | Add Survey |


  Scenario: Admin is opening site detail page
    Given I logged in as "admin"
    When I open "site detail" page with pk "10"
    Then I should see following
      | text        |
      | Gabe Newell |
      | Assign      |
      | Edit        |
      | Commit      |
    And I should see following text in following services
      | service    | text                             |
      | potable    | Jan. 26, 2015                    |
      | potable    | Add Survey                       |
      | fire       | Fire water supply is not present |
      | irrigation | Add Survey                       |
    And I should not see following text in following services
      | service | text       |
      | fire    | Add Survey |


  Scenario: Surveyor is opening site detail page
    Given I logged in as "surveyor"
    When I open "site detail" page with pk "10"
    Then I should see following
      | text        |
      | Gabe Newell |
      | Commit      |
    And I should not see following
      | text            |
      | Assign Surveyor |
      | Assign Tester   |
      | Edit Site       |
    And I should see following text in following services
      | service    | text                             |
      | potable    | Jan. 26, 2015                    |
      | fire       | Fire water supply is not present |
      | irrigation | Add Survey                       |
    And I should not see following text in following services
      | service | text       |
      | potable | Add Survey |
      | fire    | Add Survey |


  Scenario: Tester is opening site detail page
    Given I logged in as "tester"
    When I open "site detail" page with pk "10"
    Then I should see following
      | text        |
      | Gabe Newell |
      | Commit      |
    And I should not see following
      | text            |
      | Assign Surveyor |
      | Assign Tester   |
      | Edit Site       |
    And I should see following text in following services
      | service | text                             |
      | potable | Seattle                          |
      | fire    | Fire water supply is not present |
    And I should not see following text in following services
      | service    | text          |
      | potable    | Jan. 26, 2015 |
      | potable    | Add Survey    |
      | fire       | Add Survey    |
      | irrigation | Add Survey    |

  @commit
  Scenario Outline: Site commiting
    Given I logged in as "<role>"
    When I open "site detail" page with pk "10"
    And I commit site
    Then I should be at "site list" page
    And I should not see following
      | text               |
      | VALVE, Gabe Newell |
    And I open "site detail" page with pk "10"
    And I should see "Not Found"
    And I logout
    And Uncommit sites

    Examples:
      | role     |
      | surveyor |
      | tester   |