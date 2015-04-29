from common_steps import *
from lettuce import *
from selenium import *
from webapp.models import Site, PWS, CustomerCode
from main.parameters import STATES


TEST_SITES_COUNT = 100
TEST_CUSTOMERS_COUNT = 100


@step('I generate test sites')
def generate_test_sites(step):
    pws = PWS.objects.first()
    cust_code = CustomerCode.objects.first()
    for i in xrange(0, TEST_SITES_COUNT):
        site = Site()
        site.pws = pws
        site.address1 = 'TestAddress%s' % i
        site.city = 'TestCity%s' % i
        site.state = STATES[0][0]
        site.cust_code = cust_code
        site.cust_number = 'TNUM%s' % i
        site.zip = 'TestZip%s' % i
        site.save()


@step('I delete test sites')
def delete_test_sites(step):
    Site.objects.filter(city__startswith='TestCity').delete()


@step('I turn to the "(\d+)" page')
def click_pagination_link(step, page_number):
    link = helper.find(Xpath.Pattern.pagination_link % page_number)
    helper.check_element_exists(link, 'Pagination link with page number "%s" was not found' % page_number)
    link.click()