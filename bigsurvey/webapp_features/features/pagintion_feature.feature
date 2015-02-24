@pagination
Feature: Pagination


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


  Scenario: Customer pagination
    Given I logged in as "root"
    And I generate test customers
    When I open "customer_list" page
    Then I should see following
      | text         |
      | TestNumber0  |
      | TestNumber40 |
    And I should not see following
      | text         |
      | TestNumber42 |
    When I turn to the "2" page
    Then I should see following
      | text         |
      | TestNumber42 |
      | TestNumber90 |
    And I should not see following
      | text         |
      | TestNumber92 |
    When I turn to the "3" page
    Then I should see following
      | text         |
      | TestNumber92 |
      | TestNumber99 |
    Then I delete test customers