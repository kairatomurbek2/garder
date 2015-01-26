Feature: Menu

    Scenario Outline: Menu
        Given I open "login" page
        When I login as "<role>"
        Then I should <reaction> elements with id="<ids>"

    Examples:
        | role     | reaction | ids                                                                                                       |
        | root     | see      | admin_link :: pws_link :: customers_link :: letters_link :: selectables_link :: import_link :: sites_link |
        | admin    | see      | customers_link :: letters_link :: selectables_link :: import_link :: sites_link                           |
        | admin    | not see  | admin_link :: pws_link                                                                                    |
        | surveyor | see      | sites_link                                                                                                |
        | surveyor | not see  | admin_link :: pws_link :: customers_link :: letters_link :: selectables_link :: import_link               |
        | tester   | see      | sites_link                                                                                                |
        | tester   | not see  | admin_link :: pws_link :: customers_link :: letters_link :: selectables_link :: import_link               |
