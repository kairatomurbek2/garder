@menu
Feature: Menu


  Scenario: Root Menu
    Given I logged in as "root"
    And I open "home" page
    When I hover on "more" link
    Then I should see following menu links
      | link            |
      | admin           |
      | pws             |
      | letters         |
      | import          |
      | sites           |
      | surveys         |
      | tests           |
      | hazards         |
      | testers         |
      | users           |


  Scenario: Admin Menu
    Given I logged in as "admin"
    When I open "home" page
    When I hover on "more" link
    Then I should see following menu links
      | link            |
      | letters         |
      | import          |
      | sites           |
      | surveys         |
      | tests           |
      | hazards         |
      | testers         |
      | users           |
    And I should not see following menu links
      | link  |
      | admin |
      | pws   |


  Scenario: Surveyor Menu
    Given I logged in as "surveyor"
    When I open "home" page
    Then I should see following menu links
      | link    |
      | sites   |
      | surveys |
      | letters |
      | hazards |
    And I should not see following menu links
      | link            |
      | tests           |
      | pws             |
      | import          |
      | users           |
      | testers         |


  Scenario: Tester Menu
    Given I logged in as "tester"
    When I open "home" page
    Then I should see following menu links
      | link    |
      | sites   |
      | tests   |
      | hazards |
    And I should not see following menu links
      | link            |
      | admin           |
      | pws             |
      | letters         |
      | import          |
      | users           |
      | surveys         |
      | testers         |