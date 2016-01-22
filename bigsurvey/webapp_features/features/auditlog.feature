@auditlog
Feature: Audit Logging

  @keep_db
  Scenario: PWS owner sees only their own PWS audit log records
    Given Owner of the following PWSs changes username of "testPWStester" user to "testPWStester1":
      | PWS name |
      | testPWS  |
    When Owner of the following PWSs goes to auditlog page:
      | PWS name        |
      | White House PWS |
      | North USA PWS   |
    Then there are no auditlog records displayed on the page
    But Owner of the following PWSs goes to auditlog page:
      | PWS name |
      | testPWS  |
    And sees the following record:
      | User   | Groups    | Object               | Changes        |
      | owner2 | PWSOwners | User: testPWStester1 | testPWStester1 |


  Scenario: Filtering by username
    Given surveyor edited site "RAL1234-14"
    And owner edited site "VALVE"
    When owner filters auditlog by username "surveyor"
    Then he sees the following record:
      | User     | Groups    | PWS                   | Object                          | Changes      |
      | surveyor | Surveyors | NUI812, North USA PWS | Site: 72 Mial st, Raleigh 27601 | fire_present |
    But does not see changes made by owner


  Scenario: Filtering by group
    Given Given surveyor edited site "RAL1234-14"
    And And owner edited site "VALVE"
    When owner filters auditlog by user group "Surveyors"
    Then he sees the following record:
      | User     | Groups    | PWS                   | Object                          | Changes      |
      | surveyor | Surveyors | NUI812, North USA PWS | Site: 72 Mial st, Raleigh 27601 | fire_present |
    But does not see changes made by owner
