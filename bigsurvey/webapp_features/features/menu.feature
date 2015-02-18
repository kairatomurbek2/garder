@menu
Feature: Menu


  Scenario: Root Menu
    Given I logged in as "root"
    And I open "home" page
    When I hover on "menu" link
    Then I should see following menu links
      | link            |
      | admin           |
      | pws             |
      | customers       |
      | letters         |
      | import          |
      | sites           |
      | inspections     |
      | testpermissions |
      | users           |


  Scenario: Admin Menu
    Given I logged in as "admin"
    When I open "home" page
    When I hover on "menu" link
    Then I should see following menu links
      | link            |
      | customers       |
      | letters         |
      | import          |
      | sites           |
      | inspections     |
      | testpermissions |
      | users           |
    And I should not see following menu links
      | link  |
      | admin |
      | pws   |


  Scenario: Surveyor Menu
    Given I logged in as "surveyor"
    When I open "home" page
    When I hover on "menu" link
    Then I should see following menu links
      | link  |
      | sites |
    And I should not see following menu links
      | link            |
      | admin           |
      | pws             |
      | customers       |
      | letters         |
      | import          |
      | inspections     |
      | testpermissions |
      | users           |


  Scenario: Tester Menu
    Given I logged in as "tester"
    When I open "home" page
    When I hover on "menu" link
    Then I should see following menu links
      | link  |
      | sites |
    And I should not see following menu links
      | link            |
      | admin           |
      | pws             |
      | customers       |
      | letters         |
      | import          |
      | inspections     |
      | testpermissions |
      | users           |