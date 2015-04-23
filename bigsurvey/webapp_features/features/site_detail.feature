@site_detail
Feature: Site detail


  Scenario Outline: Site detail page access
    Given I logged in as "<role>"
    When I directly open "site_detail" page with pk "<pk>"
    Then I should <reaction> "Not Found"
    And I logout
  Examples:
    | role     | pk | reaction |
    | root     | 3  | not see  |
    | root     | 4  | not see  |
    | admin    | 3  | see      |
    | admin    | 4  | not see  |
    | surveyor | 3  | see      |
    | surveyor | 4  | not see  |
    | tester   | 3  | see      |
    | tester   | 9  | not see  |


  Scenario: Root is opening site detail page
    Given I logged in as "root"
    When I open "site_detail" page with pk "10"
    Then I should see following
      | text                 |
      | Gabe Newell          |
      | Edit                 |
      | Surveys              |
      | Hazards              |
      | 98, South Jackson st |
      | 75/2                 |
      | 7269                 |
      | VALVE-APT            |
      | 127, Universe st     |
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
    When I open "site_detail" page with pk "10"
    Then I should see following
      | text        |
      | Gabe Newell |
      | Edit        |
      | Surveys     |
      | Hazards     |
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
    When I open "site_detail" page with pk "10"
    Then I should see following
      | text        |
      | Gabe Newell |
      | Surveys     |
      | Hazards     |
    And I should not see following
      | text |
      | Edit |
    And I should see following text in following services
      | service    | text                             |
      | potable    | Jan. 26, 2015                    |
      | potable    | Add Survey                       |
      | fire       | Fire water supply is not present |
      | irrigation | Add Survey                       |
    And I should not see following text in following services
      | service | text       |
      | fire    | Add Survey |


  Scenario: Tester is opening site detail page
    Given I logged in as "tester"
    When I open "site_detail" page with pk "10"
    Then I should see following
      | text        |
      | Gabe Newell |
      | Hazards     |
    And I should not see following
      | text    |
      | Edit    |
      | Surveys |
    And I should see following text in following hazard services
      | service | text                             |
      | potable | Seattle                          |
      | fire    | Fire water supply is not present |