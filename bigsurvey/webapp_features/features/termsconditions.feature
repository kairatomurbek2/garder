Feature: Term and Condition

  Scenario: Addition Term and Condition
    Given Im on a page to add terms conditions
    And I fill in file input "pdf_file" with "tos.pdf"
    And I submit form
    When I turn to the list of terms conditions
    And I see the added file
    Then I deleted "tos.pdf"

  Scenario: Checking for validation
    Given Im on a page to add terms conditions
    And I fill in file input "pdf_file" with "logo.jpg"
    And I submit form
    Then I see an error "PDF file required"