@pws
@pws_detail
Feature: PWS Detail Page
  @keep_db
  Scenario Outline: PWS Detail Page access
    Given I logged in as "<role>"
    When I directly open "pws_detail" page with pk "<pk>"
    Then I should <reaction> "Page not found"
  Examples:
    | role      | pk | reaction |
    | root      | 1  | not see  |
    | root      | 9  | not see  |
    | admin     | 1  | see      |
    | admin     | 9  | not see  |
    | surveyor  | 1  | see      |
    | surveyor  | 9  | see      |
    | tester    | 1  | see      |
    | tester    | 9  | see      |
    | root      | 6  | not see  |
    | admin     | 6  | see      |
    | pws_owner | 1  | see      |
    | pws_owner | 6  | not see  |
    | pws_owner | 9  | not see  |
    | surveyor  | 6  | see      |
    | tester    | 6  | see      |

  @keep_db
  Scenario: PWS Detail Page elements
    Given I logged in as "root"
    When I open "pws_detail" page with pk "9"
    Then I should see following
      | text                                 |
      | North USA PWS                        |
      | 200 South Jefferson st.              |
      | Public Water Supply and Private Well |
      | Chikago                              |
      | IL                                   |
      | +987654321                           |
      | John McConley                        |
      | pws@test.com                         |
      | Van der Veijden                      |
      | +1685231452                          |