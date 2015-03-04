@last_survey_date
Feature: last survey date


  Scenario: I See initial date
    Given I logged in as "root"
    When I open "site_list" page
    Then I should see following
      | March 5, 2011 |

  Scenario: I change the date to the new date
    Given I logged in as "root"
    When I open "survey_add" page for site with pk "3" and service "potable"
    And I fill in "survey_date" with "2015-03-10"
    And I select "surveyor" from "surveyor"
    And I submit "survey" form
    Then I should be at "survey_detail" page with pk "3"
    And I should see following
      | March 10, 2015 |

  Scenario: I can change the date to the old date
    Given I logged in as "root"
    When I open "site_detail" page with pk "3"
    And I open "survey_edit" page for "1" survey on the page
    And I fill in "survey_date" with "2011-03-05"
    And I select "surveyor" from "surveyor"
    And I submit "survey" form
    And I open "site_detail" page with pk "3"
    Then I should see following
      | March 5, 2011 |

