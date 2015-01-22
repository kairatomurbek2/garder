Feature: Filtration

    Scenario Outline: Filtration
        Given I open login page
        And I login as <role>
        And I open site_list page
        When I fill many <fields> with <values>
        And I submit site_filter form
        Then I <reaction> - <site> on page

    Examples:
        | role     | fields        | values     | reaction   | site                    |
        | root     | city          | on         | see        | Second Site             |
        | root     | city          | on         | see        | Houston                 |
        | root     | city          | on         | do not see | Ancoridge               |
        | root     | city,customer | on,matt    | see        | MIT Public Water System |
        | root     | city,site_use | chik,indus | see        | Giles Corey             |
        | root     | address1      | cent       | see        | Ancoridge               |
        | root     | site_type     | qwerty     | do not see | Assign                  |
        | admin    | site_use      | ind        | see        | Chikago                 |
        | admin    | site_use      | ind        | do not see | Boston                  |
        | surveyor | pws           | north      | see        | Seattle                 |
        | surveyor | pws           | north      | do not see | Chikago                 |
        | tester   | site_type     | govern     | see        | New York                |
        | tester   | site_type     | govern     | do not see | Washington              |