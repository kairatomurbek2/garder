@customer_list
Feature: Customer list

  Scenario Outline: Customer list page access
    Given I logged in as "<role>"
    When I directly open "customer_list" page
    Then I should <reaction> "Not Found"
    And I logout
  Examples:
    | role     | reaction |
    | root     | not see  |
    | admin    | not see  |
    | surveyor | see      |
    | tester   | see      |


  Scenario: Root is opening customer list page
    Given I logged in as "root"
    When I open "customer_list" page
    Then I should see following
      | text          |
      | John Smith    |
      | Mike Doe      |
      | Amanda James  |
      | Jane Asperson |
      | Matt Asperson |
      | Giles Corey   |
      | Gabe Newell   |


  Scenario: Admin is opening customer list page
    Given I logged in as "admin"
    When I open "customer_list" page
    Then I should see following
      | text          |
      | John Smith    |
      | Mike Doe      |
      | Amanda James  |
      | Jane Asperson |
      | Matt Asperson |
      | Giles Corey   |
      | Gabe Newell   |