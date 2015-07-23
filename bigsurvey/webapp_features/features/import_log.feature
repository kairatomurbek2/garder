@import_log
Feature: Import Log

  Scenario: Added sites label exists
    Given The is performed import from "2015-07-21 12:27" by "root" into "NUI812"
    And I logged in as "root"
    When I open added sites of this import
    Then I should see added sites notification of this import

  Scenario: Updated sites label exists
    Given The is performed import from "2015-07-21 12:27" by "root" into "NUI812"
    And I logged in as "root"
    When I open updated sites of this import
    Then I should see updated sites notification of this import

  Scenario: Deactivated sites label exists
    Given The is performed import from "2015-07-21 12:27" by "root" into "NUI812"
    And I logged in as "root"
    When I open deactivated sites of this import
    Then I should see deactivated sites notification of this import