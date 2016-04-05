@test_payment
Feature: Test payment
  @keep_db
  Scenario: Unpaid test is not visible on site
    Given I logged in as "root"
    When I open "hazard_detail" page with pk "1"
    Then I should not see "June 1, 2015, Failed"

  @payment_for_test
  Scenario: Payment for test
    Given I logged in as "tester"
    And I open "unpaid_test_list" page"
    When I check "4" from "tests"
    And I click "pay" button
    And I click "payment_creation" link
    And I wait until step 2 is appeared
    And I click "approval" link
    And click url
    And I login in PayPal
    And I confirm payment
    Then I should be redirected to "unpaid_test_list" page
    And I should see "payment successful" message
    When I directly open "hazard_detail" page with pk "2"
    Then I should see "Jan. 27, 2015, Failed"