@customer_filter
Feature: Customer list filtering


  Scenario: Filter by Account Number
    Given I logged in as "root"
    And I open "customer_list" page
    When I fill in "number" with "I"
    And I submit "customer_filter" form
    Then I should see following
      | text   |
      | IKW182 |
      | MIA281 |
      | OIK182 |
    And I should not see following
      | text      |
      | Customer1 |
      | ZXC2      |
      | SJK472    |

  Scenario: Filter by Customer Name
    Given I logged in as "root"
    And I open "customer_list" page
    When I fill in "name" with "Asper"
    And I submit "customer_filter" form
    Then I should see following
      | text   |
      | IKW182 |
      | MIA281 |
    And I should not see following
      | text      |
      | Customer1 |
      | ZXC2      |
      | SJK472    |
      | OIK182    |

  Scenario: Filter by Customer Code
    Given I logged in as "root"
    And I open "customer_list" page
    When I select "4" from "code"
    And I submit "customer_filter" form
    Then I should see following
      | text   |
      | SJK472 |
      | MIA281 |
    And I should not see following
      | text      |
      | Customer1 |
      | ZXC2      |
      | OIK182    |

  Scenario: Filter by City
    Given I logged in as "root"
    And I open "customer_list" page
    When I fill in "city" with "An"
    And I submit "customer_filter" form
    Then I should see following
      | text   |
      | SJK472 |
      | IKW182 |
    And I should not see following
      | text      |
      | Customer1 |
      | ZXC2      |
      | OIK182    |

  Scenario: Filter by Address
    Given I logged in as "root"
    And I open "customer_list" page
    When I fill in "address" with "8"
    And I submit "customer_filter" form
    Then I should see following
      | text   |
      | MIA281 |
      | OIK182 |
    And I should not see following
      | text      |
      | Customer1 |
      | ZXC2      |
      | SJK472    |
      | IKW182    |

  Scenario: Filter by ZIP
    Given I logged in as "root"
    And I open "customer_list" page
    When I fill in "zip" with "21"
    And I submit "customer_filter" form
    Then I should see following
      | text   |
      | SJK472 |
      | IKW182 |
      | MIA281 |
      | OIK182 |
    And I should not see following
      | text      |
      | Customer1 |
      | ZXC2      |

  Scenario: Filter by multiple fields
    Given I logged in as "root"
    And I open "customer_list" page
    When I select "2" from "code"
    When I fill in following fields with following values
      | field  | value |
      | number | Q     |
      | name   | e     |
      | zip    | 9     |
    And I submit "customer_filter" form
    Then I should see following
      | text    |
      | QAZ2WSX |
    And I should not see following
      | text      |
      | Customer1 |
      | ZXC2      |
      | SJK472    |
      | IKW182    |
      | MIA281    |
      | OIK182    |