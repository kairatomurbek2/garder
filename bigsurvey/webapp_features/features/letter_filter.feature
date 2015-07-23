@letter
@letter_filter
Feature: Letter Filtration

  @keep_db
  Scenario: LetterFiltration
    Given I logged in as "root"
    And I open "letter_list" page
    When I fill in following fields with following values
      | field          | value      |
      | customer       | QAZ2WSX    |
      | customer_email | hotmail    |
      | user           | oo         |
      | date_gt        | 2015-05-03 |
      | date_lt        | 2015-05-03 |
    And I select "DOC121" from "pws"
    And I select "potable" from "service_type"
    And I select "Denied or Restricted Access" from "hazard_type"
    And I select "Air Gap" from "letter_type"
    And I select "No" from "already_sent"
    And I submit "letter_filter" form
    Then I should see following
      | text        |
      | QAZ2WSX     |
      | May 3, 2015 |
    And I should not see following
      | text        |
      | May 5, 2015 |
      | VALVE       |