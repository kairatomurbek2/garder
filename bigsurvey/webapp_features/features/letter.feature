@letter
@letter_detail
Feature: Letter Viewing and Sending

  @letter_detail_page_access
  Scenario Outline: Letter Detail Page Access
    Given I logged in as "<role>"
    When I directly open "letter_detail" page with pk "<pk>"
    Then I should <reaction> "Page not found"
    And I logout
  Examples:
    | role     | pk | reaction |
    | root     | 1  | not see  |
    | root     | 2  | not see  |
    | admin    | 1  | see      |
    | admin    | 2  | not see  |
    | surveyor | 1  | see      |
    | surveyor | 2  | not see  |
    | tester   | 1  | see      |
    | tester   | 2  | see      |

  Scenario: Letter Detail Page Elements
    Given I logged in as "root"
    When I open "letter_detail" page with pk "2"
    Then I should see warning letter message
    And I should see following
      | text                                |
      | Send to                             |
      | May 05, 2015                        |
      | {AssemblyType}                      |
      | {DueDate}                           |
      | Seattle, WA, 12382                  |
      | 7269, South Jackson st, Seattle, WA |
      | +1685231452                         |
      | Sincerely, John McConley            |
      | Director of Public Works            |
      | Van der Veijden                     |
      | Edit                                |
      | Get PDF                             |
      | +123456789                          |
      | +987654321                          |
      | pws@test.com                        |
      | 200 South Jefferson st.             |
      | Chikago, IL, 70643                  |