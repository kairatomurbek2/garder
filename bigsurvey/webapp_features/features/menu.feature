@menu
Feature: Menu
  @keep_db
  Scenario: Root Menu
    Given I logged in as "root"
    And I open "home" page
    Then I should see following menu links
      | link    |
      | admin   |
      | pws     |
      | letters |
      | import  |
      | sites   |
      | surveys |
      | tests   |
      | hazards |
      | testers |
      | users   |

  @keep_db
  Scenario: Admin Menu
    Given I logged in as "admin"
    When I open "home" page
    Then I should see following menu links
      | link         |
      | letters      |
      | import       |
      | sites        |
      | surveys      |
      | tests        |
      | hazards      |
      | testers      |
      | users        |
    And I should not see following menu links
      | link  |
      | admin |

  @keep_db
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
      | link    |
      | tests   |
      | pws     |
      | import  |
      | users   |
      | testers |

  @keep_db
  Scenario: Tester Menu
    Given I logged in as "tester"
    When I open "home" page
    Then I should see following menu links
      | link  |
      | sites |
      | tests |
    And I should not see following menu links
      | link    |
      | admin   |
      | pws     |
      | letters |
      | import  |
      | users   |
      | surveys |
      | testers |

  @keep_db\
  Scenario: PWS owner menu
    Given I logged in as "pws_owner"
    When I open "home" page
    Then I should see following menu links
    Then I should see following menu links
      | link    |
      | letters |
      | import  |
      | sites   |
      | surveys |
      | tests   |
      | hazards |
      | testers |
      | users   |
      | pws     |
    And I should not see following menu links
      | link  |
      | admin |
