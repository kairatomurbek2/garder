@letter
@letter_list
Feature: Letter List

  Scenario Outline: Letter List Page Access
    Given I logged in as "<role>"
    When I directly open "letter_list" page
    Then I should <reaction> "Not Found"
    And I logout
  Examples:
    | role     | reaction |
    | root     | not see  |
    | admin    | not see  |
    | surveyor | not see  |
    | tester   | see      |

  Scenario: Root is opening letter list page
    Given I logged in as "root"
    When I open "letter_list" page
    Then I should see following
      | text                  |
      | DOC121                |
      | Filters               |
      | QAZ2WSX               |
      | amanda_j@hotmail.com  |
      | potable               |
      | Denied or Restricted  |
      | Air Gap               |
      | root                  |
      | No                    |
      | thesomeq@gmail.com    |
      | May 5, 2015           |
      | Show                  |
      | PDF                   |
      | NUI812                |

  Scenario: Admin is opening letter list page
    Given I logged in as "admin"
    When I open "letter_list" page
    Then I should see following
      | text                  |
      | VALVE                 |
      | None                  |
      | potable               |
      | Trailer Park          |
      | Annual Test Second    |
      | root                  |
      | No                    |
      | thesomeq@gmail.com    |
      | May 5, 2015           |
      | Show                  |
      | PDF                   |
    And I should not see following
      | text                  |
      | amanda_j@hotmail.com  |
      | NUI812                |

  Scenario: Surveyor is opening letter list page
    Given I logged in as "surveyor"
    When I open "letter_list" page
    Then I should see following
      | text                  |
      | VALVE                 |
      | None                  |
      | potable               |
      | Trailer Park          |
      | Annual Test Second    |
      | root                  |
      | No                    |
      | thesomeq@gmail.com    |
      | May 5, 2015           |
      | Show                  |
      | PDF                   |
    And I should not see following
      | text                  |
      | amanda_j@hotmail.com  |
      | NUI812                |