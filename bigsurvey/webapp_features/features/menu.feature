@menu
Feature: Menu


  Scenario: Root Menu
    Given I logged in as "root"
    When I open "home" page
    Then I should see following menu links
      | link      |
      | admin     |
      | pws       |
      | customers |
      | letters   |
      | import    |
      | sites     |


  Scenario: Admin Menu
    Given I logged in as "admin"
    When I open "home" page
    Then I should see following menu links
      | link      |
      | customers |
      | letters   |
      | import    |
      | sites     |
    And I should not see following menu links
      | link  |
      | admin |
      | pws   |


  Scenario: Surveyor Menu
    Given I logged in as "surveyor"
    When I open "home" page
    Then I should see following menu links
      | link  |
      | sites |
    And I should not see following menu links
      | link      |
      | admin     |
      | pws       |
      | customers |
      | letters   |
      | import    |


  Scenario: Tester Menu
    Given I logged in as "tester"
    When I open "home" page
    Then I should see following menu links
      | link  |
      | sites |
    And I should not see following menu links
      | link      |
      | admin     |
      | pws       |
      | customers |
      | letters   |
      | import    |