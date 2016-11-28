@tester
@tester_filter
Feature: Tester Filtration

  @keep_db
  Scenario: TesterFiltration
    Given I logged in as "root"
    And I open "tester_list" page
    When I fill in following fields with following values
      | field       | value              |
      | username    | tester             |
      | name        | tester             |
      | company     | tester company     |
      | email       | tester@example.com |
      | cert_number | qwerty132          |
      | test_serial | serial1            |
    And I select "NUI812" from "pws"
    And I submit "tester_filter" form
    Then I should see following
      | text   |
      | NUI812 |
      | tester |
    And I should not see following
      | text               |
      | tester_without_pws |
      | nopws@tester.com   |