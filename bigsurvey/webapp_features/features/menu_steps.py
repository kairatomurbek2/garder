from common_steps import *
from lettuce import *
from settings import *


@step('I should see following menu links')
def check_menu_links_exist(step):
    for row in step.hashes:
        link = helper.find(Xpath.Pattern.menu_link % row['link'])
        helper.check_element_exists(link, '"%s" link is not in menu' % row['link'])


@step('I should not see following menu links')
def check_menu_links_dont_exist(step):
    for row in step.hashes:
        link = helper.find(Xpath.Pattern.menu_link % row['link'])
        helper.check_element_doesnt_exist(link, '"%s" link is in menu' % row['link'])