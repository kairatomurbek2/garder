@last_survey_date
Feature: last survey date

  Scenario: I See initial date
    Given I logged in as "root"
    When I open "site_list" page
    Then I should see following
      | text          |
      | Jan. 26, 2015 |
    And I should not see following
      | text          |
      | Jan. 27, 2015 |

  Scenario: I add survey with newer date
    Given I logged in as "root"
    When I open "survey_add" page for site with pk "10" and service "potable"
    And I fill in "survey_date" with "2015-01-27"
    And I select "surveyor" from "surveyor"
    And I submit "survey" form
    And I open "site_list" page
    Then I should see following
      | text          |
      | Jan. 27, 2015 |

  Scenario: I change survey date to older date
    Given I logged in as "root"
    When I open "site_detail" page with pk "10"
    And I open "survey_edit" page for survey no "2" on the page
    And I fill in "survey_date" with "2015-01-25"
    And I submit "survey" form
    And I open "site_list" page
    Then I should see following
      | text          |
      | Jan. 26, 2015 |
    And I should not see following
      | text          |
      | Jan. 27, 2015 |
      | Jan. 25, 2015 |

