@bp_device
Feature: BPDevice adding/editing
  
  Scenario: Surveyor adds bp-device while adding hazard in survey
    Given I logged in as "surveyor"
    And I open "hazard_add" page for site with pk "10" and service "potable"
    When I select "Aspirator" from "hazard_type"
    And I select "Installed" from "assembly_status"
    And I select "AVB" from "bp-bp_type_present"

  Scenario: Surveyor edits bp-device while editing hazard
  
  
  Scenario: Tester installs bp-device on hazard
  
  
  Scenario: Tester replaces bp-device on hazard
  
  
  Scenario: Tester with no licence can not install or replace bp-device
