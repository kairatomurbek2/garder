@hazard_detail
Feature: Hazard Detail
  @keep_db
  Scenario Outline: Hazard detail page access
    Given I logged in as "<role>"
    When I directly open "hazard_detail" page with pk "<pk>"
    Then I should <reaction> "Page not found"

  Examples:
    | role     | pk | reaction |
    | root     | 1  | not see  |
    | root     | 2  | not see  |
    | root     | 4  | not see  |
    | admin    | 2  | not see  |
    | admin    | 1  | see      |
    | admin    | 4  | see      |
    | pws_owner| 1  | not see  |
    | pws_owner| 2  | not see  |
    | pws_owner| 4  | see      |
    | surveyor | 2  | not see  |
    | surveyor | 1  | see      |
    | surveyor | 4  | see      |
    | tester   | 2  | not see  |
    | tester   | 1  | not see  |
    | tester   | 4  | see      |

  @keep_db
  Scenario: Hazard detail page elements
    Given I logged in as "root"
    When I open "hazard_detail" page with pk "1"
    Then I should see following
      | text                          |
      | White House, Washington 80192 |
      | irrigation                    |
      | Digester                      |
      | Location 1                    |
      | Installer                     |
      | Feb. 18, 2015                 |
      | Edit                          |
      | Add Test                      |
      | Jan. 27, 2015, Failed         |
      | Pump Present                  |
      | CC Present                    |
      | Additives Present             |
      | Auxiliary Water               |