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
        | tester   | 10     | not see  | Assign Surveyor :: Assign Tester :: Edit Site                |
