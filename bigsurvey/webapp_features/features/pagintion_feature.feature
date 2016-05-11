@pagination
Feature: Pagination

  Scenario: Site pagination
    Given I logged in as "root"
    And I generate test sites
    When I open "site_list" page
    Then I should see following
      | text       |
      | TestCity99 |
      | TestCity92 |
    And I should not see following
      | text       |
      | TestCity48 |
    When I turn to the "2" page
    Then I should see following
      | text       |
      | TestCity48 |
      | TestCity49 |
    And I should not see following
      | text       |
      | TestCity97 |
    When I turn to the "3" page
    Then I should see following
      | text    |
      | Raleigh |
      | Seattle |