@letter
@letter_list
Feature: Letter List

  @keep_db
  Scenario Outline: Letter List Page Access
    Given I logged in as "<role>"
    When I directly open "letter_list" page
    Then I should <reaction> "Page not found"
  Examples:
    | role      | reaction |
    | root      | not see  |
    | admin     | not see  |
    | pws_owner | not see  |
    | surveyor  | not see  |
    | tester    | see      |

  @keep_db
  Scenario: Root is opening letter list page
    Given I logged in as "root"
    When I open "letter_list" page
    Then I should see following
      | text                  |
      | DOC121                |
      | PWS2                  |
      | Filters               |
      | QAZ2WSX               |
      | amanda_j@hotmail.com  |
      | potable               |
      | Denied or Restricted  |
      | Air Gap               |
      | root                  |
      | No                    |
      | May 5, 2015           |
      | Show                  |
      | PDF                   |
      | NUI812                |

  @keep_db
  @owner_letter_list
  Scenario: Pws owner is opening letter list page
    Given I logged in as "pws_owner"
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
      | May 5, 2015           |
      | Show                  |
      | PDF                   |
      | NUI812                |
    And I should not see following
      | text                  |
      | Customer1             |

  @keep_db
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
      | May 5, 2015           |
      | Show                  |
      | PDF                   |
    And I should not see following
      | text                  |
      | amanda_j@hotmail.com  |
      | PWS2                  |

  @keep_db
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
      | May 5, 2015           |
      | Show                  |
      | PDF                   |
    And I should not see following
      | text                  |
      | amanda_j@hotmail.com  |
      | PWS2                  |