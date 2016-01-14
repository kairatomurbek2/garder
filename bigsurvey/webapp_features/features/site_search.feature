@site_search
Feature: Site search

  @keep_db
  Scenario Outline: Search by fields
    Given I logged in as "tester"
    When I select "PWS3, Third PWS" from "pws"
    And I fill in "<field>" with "<search_term>"
    And I submit "tester-site-search" form
    Then I should see the following link: "<site_link>"

    Examples:
      | field        | search_term | site_link                                                                     |
      | address      | 18          | 18/12, Central Square, Ancoridge 39012 Customer number: SJK472                |
      | cust_number  | OIK182      | 121, Broadview, Chikago 00192 Customer number: OIK182 Meter number: 123456789 |
      | meter_number | 321654987   | 72 Mial st, Raleigh 27601 Customer number: RAL1234-14 Meter number: 321654987 |
