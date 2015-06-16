@letter_send
Feature: Sending letters

  Scenario: Sending letters with testers list and consultant info
    Given I logged in as "root"
    And I open "letter_detail" page with pk "2"
    When I fill in "send_to" with "customer@example.com"
    And I check "attach_testers"
    And I check "attach_consultant_info"
    And I submit "letter-send" form
    Then Receiver "customer@example.com" should receive email
    And Email should contain following text
      | text               |
      | Van der Veijden    |
      | +1685231452        |
      | tester tester      |
      | tester@example.com |