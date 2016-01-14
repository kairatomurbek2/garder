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


  @keep_db
  Scenario: Search by address returns all sites with addresses containing the search term
    Given I logged in as "tester"
    When I select "PWS3, Third PWS" from "pws"
    And I fill in "address" with "2"
    And I submit "tester-site-search" form
    Then I should see the following links in search result:
    | site_link                                                                     |
    | 18/12, Central Square, Ancoridge 39012 Customer number: SJK472                |
    | 121, Broadview, Chikago 00192 Customer number: OIK182 Meter number: 123456789 |
    | 72 Mial st, Raleigh 27601 Customer number: RAL1234-14 Meter number: 321654987 |


  @keep_db
  Scenario Outline: Search with pws field unfilled
    Given I logged in as "tester"
    And I fill in "<filled_field>" with "2"
    When I submit "tester-site-search" form
    Then I should see the following error message above "PWS" field:
      | error_message           |
      | This field is required. |

  Examples:
    | filled_field |
    | address      |
    | cust_number  |
    | meter_number |

  @keep_db
  Scenario: Search with only pws field filled
    Given I logged in as "tester"
    When I select "PWS3, Third PWS" from "pws"
    And I submit "tester-site-search" form
    Then I should see the following error message above "Street number and address", "Customer Number" and "Meter Number" fields
      | error_message                                                                                                              |
      | Besides PWS, at least one of the following fields must be filled: Street number and address, Customer number, Meter number |


  @keep_db
  Scenario: Search by customer number is case insensitive
    Given I logged in as "tester"
    When I select "PWS3, Third PWS" from "pws"
    And I fill in "cust_number" with "oik182"
    And I submit "tester-site-search" form
    Then I should see the following link: "121, Broadview, Chikago 00192 Customer number: OIK182 Meter number: 123456789"


  @keep_db
  Scenario Outline: When searching by Customer number and Meter number search term sould match the whole value
    Given I logged in as "tester"
    And I select "PWS3, Third PWS" from "pws"
    When I fill in "<field>" with "<partial_search_term>"
    And I submit "tester-site-search" form
    Then I see no search results
    But I fill in "<field>" with "<full_search_term>"
    And I submit "tester-site-search" form
    Then I should see the following link: "<site_link>"

    Examples:
      | field        | full_search_term | partial_search_term | site_link                                                                     |
      | cust_number  | OIK182           | OIK                 | 121, Broadview, Chikago 00192 Customer number: OIK182 Meter number: 123456789 |
      | meter_number | 321654987        | 321                 | 72 Mial st, Raleigh 27601 Customer number: RAL1234-14 Meter number: 321654987 |