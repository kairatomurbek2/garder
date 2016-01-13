Feature: User Password Reset

  Scenario: User successfully create a new password through the login page
    Given user with email "tester@example.com" reset password from the login page
    When user clicks on a link with a unique token to email
    And sets a new password "12345"
    Then user "tester" and password "12345" may enter in page
