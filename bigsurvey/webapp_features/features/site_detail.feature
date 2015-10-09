@site_detail
Feature: Site detail

  @keep_db
  Scenario Outline: Site detail page access
    Given I logged in as "<role>"
    When I directly open "site_detail" page with pk "<pk>"
    Then I should <reaction> "Page not found"
  Examples:
    | role      | pk | reaction |
    | root      | 3  | not see  |
    | root      | 4  | not see  |
    | admin     | 3  | see      |
    | admin     | 4  | not see  |
    | surveyor  | 3  | see      |
    | surveyor  | 4  | not see  |
    | root      | 5  | not see  |
    | admin     | 5  | see      |
    | surveyor  | 5  | see      |
    | pws_owner | 3  | see      |
    | pws_owner | 5  | not see  |
    | pws_owner | 4  | not see  |

  @keep_db
  Scenario: Root is opening site detail page
    Given I logged in as "root"
    When I open "site_detail" page with pk "10"
    Then I should see following
      | text             |
      | Gabe Newell      |
      | Edit             |
      | Surveys          |
      | Hazards          |
      | South Jackson st |
      | 75/2             |
      | 7269             |
      | VALVE-APT        |
      | 127, Universe st |
      | surveyor         |
      | potable          |
      | Service Type     |
      | Survey type      |
      | Survey Date      |
      | Jan. 26, 2015    |

  @keep_db
  Scenario: Admin is opening site detail page
    Given I logged in as "admin"
    When I open "site_detail" page with pk "10"
    Then I should see following
      | text          |
      | Gabe Newell   |
      | Edit          |
      | Surveys       |
      | Hazards       |
      | Service Type  |
      | potable       |
      | Survey type   |
      | Annual        |
      | Survey Date   |
      | Jan. 26, 2015 |
      | surveyor      |

  @keep_db
  Scenario: Surveyor is opening site detail page
    Given I logged in as "surveyor"
    When I open "site_detail" page with pk "10"
    Then I should see following
      | text          |
      | Gabe Newell   |
      | Surveys       |
      | Hazards       |
      | Edit          |
      | Service Type  |
      | potable       |
      | Survey type   |
      | Annual        |
      | Survey Date   |
      | Jan. 26, 2015 |
      | surveyor      |

  @keep_db
  Scenario: Tester is opening site detail page
    Given I logged in as "tester"
    When I select "North USA PWS" from "pws"
    And I fill in "cust_number" with "VALVE"
    And I submit "tester-site-search" form
    Then I should be at "site_detail" page with pk "10"
    And I should see following
      | text         |
      | Gabe Newell  |
      | Hazards      |
      | Trailer Park |
      | Washington   |
      | Installed    |
    And I should not see following
      | text    |
      | Edit    |
      | Surveys |