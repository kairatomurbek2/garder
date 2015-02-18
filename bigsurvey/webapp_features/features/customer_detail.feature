@customer_detail
Feature: Customer detail


  Scenario Outline: Customer detail page access
    Given I logged in as "<role>"
    When I directly open "customer_detail" page with pk "3"
    Then I should <reaction> "Not Found"
    And I logout
  Examples:
    | role     | reaction |
    | root     | not see  |
    | admin    | not see  |
    | surveyor | see      |
    | tester   | see      |


  Scenario: Root is opening customer detail page
    Given I logged in as "root"
    When I open "customer_detail" page with pk "3"
    Then I should see following
      | text       |
      | SJK472     |
      | Ancoridge  |
      | 10, New St |
      | Mike Doe   |
      | Industrial |
      | 29021      |


  Scenario: Admin is opening customer detail page
    Given I logged in as "admin"
    When I open "customer_detail" page with pk "7"
    Then I should see following
      | text              |
      | OIK182            |
      | Chikago           |
      | 128, River Groove |
      | Giles Corey       |
      | Governmental      |
      | 19021             |