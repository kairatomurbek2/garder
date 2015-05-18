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

  @letter_detail_page_elements
  Scenario: Letter Detail Page Elements
    Given I logged in as "root"
    When I open "letter_detail" page with pk "1"
    Then I should see warning letter message
    And I should see warning due date letter message
    And I should see following
    | text                  |
    | thesomeq@gmail.com    |
    | Send                  |
    | To:                   |
    | 2015-05-03            |
    | {AssemblyType}        |
    | {DueDate}             |
    | Washington, DC, 90192 |
    | Should the customer   |
    | The City of           |
    | Thank you in advance  |
    | Sincerely,            |
    | Public Works Director |
    | I,                    |
    | agree to maintain     |
    | Customer:             |
    | Date:                 |
    | Edit                  |
    | Get PDF               |