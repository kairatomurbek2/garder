@bp_device
Feature: BPDevice adding/editing
  
  Scenario: Surveyor adds bp-device while adding hazard
    Given I logged in as "surveyor"
    And I directly open "hazard_add" page for site with pk "10" and service "potable"
    When I select "Installed" from "assembly_status"
    And I select "Aspirator" from "hazard_type"
    And I select "AVB" from "bp-bp_type_present"
    And I submit "hazard" form
    Then I should be at "hazard_detail" page with pk "5"
    Then I should see following
    | text                          |
    | Hazard was successfully added |
    | Hazard Info                   |
    | Aspirator                     |
    | BP-Device Info                |
    | AVB                           |

  Scenario: Surveyor removes bp-device from hazard
    Given I logged in as "surveyor"
    And I directly open "hazard_edit" page with pk "2"
    When I select "Due Install" from "assembly_status"
    And I submit "hazard" form
    Then I should be at "hazard_detail" page with pk "2"
    Then I should see following
    | text                            |
    | Hazard was successfully updated |
    | No Backflow Preventer present   |

  Scenario: Surveyor edits bp-device on existing hazard
    Given I logged in as "surveyor"
    And I directly open "hazard_detail" page with pk "2"
    And I should see "Edit Current BP-Device Info"
    When I click "edit_device" link
    And I fill in "notes" with "about device"
    And I submit "bp_device" form
    Then I should be at "hazard_detail" page with pk "2"
    Then I should see following
    | text                                        |
    | Backflow Preventer was successfully updated |
    | about device                                |

  @this
  Scenario: Surveyor installs bp-device on existing hazard
    Given I logged in as "surveyor"
    And Hazard with pk "2" has no bp device installed
    And I directly open "hazard_detail" page with pk "2"
    And I should see "Enter New BP-Device Info"
    When I click "install_device" link
    And I select "DC" from "bp_type_present"
    And I submit "bp_device" form
    Then I should be at "hazard_detail" page with pk "2"
    Then I should see following
    | text                                        |
    | Backflow Preventer was successfully created |
    | Assembly Type Present                       |
    | DC                                          |

  Scenario: Tester installs bp-device on hazard
    Given I logged in as "tester"
    And Hazard with pk "2" has no bp device installed
    And I open "hazard_detail" page with pk "2"
    And I click "install_device" link
    When I select "HBVB" from "bp_type_present"
    And I submit "bp_device" form
    Then I should be at "hazard_detail" page with pk "2"
    And I should see following
    | text                  |
    | Assembly Type Present |
    | HBVB                  |

  Scenario: Tester replaces bp-device on hazard
    Given I logged in as "tester"
    And I open "hazard_detail" page with pk "2"
    And I click "replace_device" link
    When I select "HBVB" from "bp_type_present"
    And I submit "bp_device" form
    Then I should be at "hazard_detail" page with pk "2"
    And I should see following
    | text                  |
    | Assembly Type Present |
    | HBVB                  |
    And I should not see "Jan. 27, 2015, Failed"

  Scenario: Tester with no licence can not install or replace bp-device
    Given Tester has no licence
    And I logged in as "tester"
    When I open "hazard_detail" page with pk "2"
    Then I should not see following
    | text                       |
    | Replace Backflow Preventer |
    And I directly open "bp_device_add" page for hazard with pk "2"
    And I should see "Page not found"