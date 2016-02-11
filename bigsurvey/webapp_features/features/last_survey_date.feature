@last_survey_date
Feature: Last survey date

  @keep_db
  Scenario: I See initial date
    Given I logged in as "root"
    When I open "site_detail" page with pk "10"
    Then I should see following
      | text          |
      | Jan. 26, 2015 |
    And I should not see following
      | text          |
      | Jan. 27, 2015 |

  Scenario: I add survey with newer date
    Given I logged in as "root"
    When I open "survey_add" page for site with pk "10" and service "potable"
    And I fill in "survey-survey_date" with "2015-01-27"
    And I select "surveyor" from "survey-surveyor"
    And I check hazard "Trailer Park"
    And I submit survey form
    And I open "site_detail" page with pk "10"
    Then I should see following
      | text          |
      | Jan. 27, 2015 |

  Scenario: I add survey with older date
    Given I logged in as "root"
    When I open "survey_add" page for site with pk "10" and service "potable"
    And I fill in "survey-survey_date" with "2015-01-24"
    And I select "surveyor" from "survey-surveyor"
    And I check hazard "Trailer Park"
    And I submit survey form
    And I open "site_list" page
    Then I should see following
      | text          |
      | Jan. 26, 2015 |
    And I should not see following
      | text          |
      | Jan. 24, 2015 |

  Scenario: I edit survey and set date
    Given I logged in as "root"
    When I open "survey_edit" page with pk "2"
    And I fill in "survey-survey_date" with "2015-01-24"
    And I submit survey form
    And I open "site_detail" page with pk "10"
    Then I should see following
      | text          |
      | Jan. 24, 2015 |
    And I should not see following
      | text          |
      | Jan. 26, 2015 |