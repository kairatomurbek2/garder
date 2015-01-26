Feature: Site detail

    Scenario Outline: Site detail
        Given I open "login" page
        And I login as "<role>"
        When I open "site_detail" page with params "<params>"
        Then I should <reaction> following "<text>"
    Examples:
        | role     | params | reaction | text                                                         |
        | root     | 10     | see      | Gabe Newell :: Assign Surveyor :: Assign Tester :: Edit Site |
        | admin    | 10     | see      | Gabe Newell :: Assign Surveyor :: Assign Tester :: Edit Site |
        | surveyor | 10     | see      | Gabe Newell :: Commit                                        |
        | surveyor | 10     | not see  | Assign Surveyor :: Assign Tester :: Edit Site                |
        | tester   | 10     | see      | Gabe Newell :: Commit                                        |
        | tester   | 10     | not see  | Assign Surveyor :: Assign Tester :: Edit Site :: Add Survey  |


    Scenario Outline: Site surveys and hazards
        Given I open "login" page
        And I login as "<role>"
        When I open "site_detail" page with params "<params>"
        Then Element with id="<id>" should <reaction> following "<text>"
    Examples:
        | role     | params | id                 | reaction    | text                                           |
        | root     | 10     | potable_content    | contain     | Jan. 26, 2015, 4:20 a.m., Annual :: Add Survey |
        | root     | 10     | fire_content       | contain     | Fire water supply is not present               |
        | root     | 10     | fire_content       | not contain | Add Survey                                     |
        | root     | 10     | irrigation_content | contain     | Add Survey                                     |
        | admin    | 10     | potable_content    | contain     | Jan. 26, 2015, 4:20 a.m., Annual :: Add Survey |
        | admin    | 10     | fire_content       | contain     | Fire water supply is not present               |
        | admin    | 10     | fire_content       | not contain | Add Survey                                     |
        | admin    | 10     | irrigation_content | contain     | Add Survey                                     |
        | surveyor | 10     | potable_content    | contain     | Jan. 26, 2015, 4:20 a.m., Annual               |
        | surveyor | 10     | potable_content    | not contain | Add Survey                                     |
        | surveyor | 10     | fire_content       | contain     | Fire water supply is not present               |
        | surveyor | 10     | irrigation_content | contain     | Add Survey                                     |
        | tester   | 10     | potable_content    | contain     | Seattle, Digester                              |
        | tester   | 10     | potable_content    | not contain | Jan. 26, 2015, 4:20 a.m., Annual               |
        | tester   | 10     | fire_content       | contain     | Fire water supply is not present               |