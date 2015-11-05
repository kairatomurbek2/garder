@site_list
Feature: Site list
  @keep_db
  Scenario: Root is opening site list page
    Given I logged in as "root"
    When I open "site_list" page
    Then I should see following sites
      | text        |
      | First Site  |
      | Second Site |
      | Houston     |
      | Ancoridge   |
      | Seattle     |
      | New York    |

  @keep_db
  @owner_site_list
  Scenario: Pws owner is opening site list page
    Given I logged in as "pws_owner"
    When I open "site_list" page
    Then I should see following sites
      | text        |
      | Ancoridge   |
      | Chikago     |
      | Seattle     |
      | New York    |
      | Washington  |
    And I should not see following sites
      | text        |
      | First Site  |
      | Second Site |
      | Houston     |
      | Boston      |

  @keep_db
  Scenario: Admin is opening site list page
    Given I logged in as "admin"
    When I open "site_list" page
    Then I should see following sites
      | text      |
      | Ancoridge |
      | Chikago   |
      | Seattle   |
    And I should not see following sites
      | text        |
      | First Site  |
      | Second Site |
      | Boston      |
      | Houston     |
      | Washington  |

  @keep_db
  Scenario: Surveyor is opening site list page
    Given I logged in as "surveyor"
    When I open "site_list" page
    Then I should see following sites
      | text       |
      | Ancoridge  |
      | Seattle    |
    And I should not see following sites
      | text        |
      | Second Site |
      | Boston      |
      | Houston     |
      | Washington  |
      | First Site  |