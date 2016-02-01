@add_pws_btn_access
Feature: Add PWS button access

  @keep_db
  Scenario Outline: Add PWS button access by user groups
    Given I logged to system as "<user>"
    When I open PWS page
    Then I can <reaction> Add PWS button

    Examples:
      | user  | reaction |
      | owner | see      |
      | admin | not see  |

