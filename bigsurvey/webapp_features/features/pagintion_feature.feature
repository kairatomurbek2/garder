@pagination
Feature: Pagination

  @site_pagination
  Scenario: Site pagination
    Given I logged in as "root"
    And I generate test sites
    When I open "site_list" page
    Then I should see following
      | text       |
      | TestCity0  |
      | TestCity38 |
    And I should not see following
      | text       |
      | TestCity40 |
    When I turn to the "2" page
    Then I should see following
      | text       |
      | TestCity40 |
      | TestCity88 |
    And I should not see following
      | text       |
      | TestCity90 |
    When I turn to the "3" page
    Then I should see following
      | text       |
      | TestCity90 |
      | TestCity99 |
    Then I delete test sites