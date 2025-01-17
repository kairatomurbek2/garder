@test_detail
Feature: Test Detail
  @keep_db
  @test_access
  Scenario Outline: Test detail page access
    Given I logged in as "<role>"
    When I directly open "test_detail" page with pk "<pk>"
    Then I should <reaction> "Page not found"
  Examples:
    | role      | pk | reaction |
    | root      | 1  | not see  |
    | root      | 2  | not see  |
    | admin     | 2  | not see  |
    | admin     | 1  | see      |
    | surveyor  | 1  | see      |
    | surveyor  | 2  | see      |
    | tester    | 2  | not see  |
    | tester    | 1  | not see  |
    | root      | 4  | see      |
    | admin     | 4  | see      |
    | surveyor  | 4  | see      |
    | tester    | 4  | not see  |
    | pws_owner | 1  | not see  |
    | pws_owner | 2  | not see  |
    | pws_owner | 4  | see      |

  @keep_db
  Scenario: Test detail page elements
    Given I logged in as "root"
    When I open "test_detail" page with pk "1"
    Then I should see following
      | text              |
      | Amanda James      |
      | White House       |
      | Internal          |
      | Spring, Air Inlet |
      | Failed            |
      | tester            |
      | qwerty132         |
      | Jan. 27, 2015     |