@auditlog
Feature: Audit Logging

  @keep_db
  Scenario: PWS owner sees only their own PWS audit log records
    Given Owner of the following PWSs changes username of tester "testPWStester" user to "testPWStester1":
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


  Scenario: Filtering by record object
    Given Given surveyor edited site "RAL1234-14"
    And And owner edited site "VALVE"
    When owner filters auditlog by record object "Raleigh"
    Then he sees the following record:
      | User     | Groups    | PWS                   | Object                          | Changes      |
      | surveyor | Surveyors | NUI812, North USA PWS | Site: 72 Mial st, Raleigh 27601 | fire_present |
    But does not see changes made by owner


  Scenario: Filtering by date range
    Given Given surveyor edited site "RAL1234-14"
    And And owner edited site "VALVE"
    When owner filters auditlog from current month start to current month ends
    Then he sees the following record:
      | User     | Groups    | PWS                   | Object                          | Changes      |
      | surveyor | Surveyors | NUI812, North USA PWS | Site: 72 Mial st, Raleigh 27601 | fire_present |
    And sees changes made by owner
    When owner filters auditlog from next month start to next month end
    Then Then he sees the following text in search results: "No records found"


  Scenario Outline: Filtering by PWS
    Given owner owns two PWSs and changes surveyors usernames:
      | PWS name                | Surveyor old username | Surveyor new username |
      | NUI812, North USA PWS   | surveyor              | surveyor1             |
      | DOC121, White House PWS | pws6user              | pws6user1             |
    When owner filters auditlog records by PWS "<pws>"
    Then owner sees "<shown>" in the search results
    But owner does not see "<hidden>" in the search results

  Examples:
    | pws                     | shown     | hidden    |
    | DOC121, White House PWS | pws6user1 | surveyor1 |
    | NUI812, North USA PWS   | surveyor1 | pws6user1 |
