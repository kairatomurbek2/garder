from lettuce import step

from webapp import models
from main.parameters import STATES, SITE_STATUS
from webapp_features.features import helper
from webapp_features.features.data import Xpath


TEST_SITES_COUNT = 100
TEST_CUSTOMERS_COUNT = 100


@step('I generate test sites')
def generate_test_sites(step):
    pws = models.PWS.objects.first()
    cust_code = models.CustomerCode.objects.first()
    active_status = models.SiteStatus.objects.get(site_status=SITE_STATUS.ACTIVE)
    for i in xrange(0, TEST_SITES_COUNT):
        site = models.Site()
        site.pws = pws
        site.address1 = 'TestAddress%s' % i
        site.city = 'TestCity%s' % i
        site.state = STATES[0][0]
        site.cust_code = cust_code
        site.cust_number = 'TNUM%s' % i
        site.zip = 'TestZip%s' % i
        site.status = active_status
        site.save()


@step('I turn to the "(\d+)" page')
def click_pagination_link(step, page_number):
    link = helper.find(Xpath.Pattern.pagination_link % page_number)
    helper.check_element_exists(link, 'Pagination link with page number "%s" was not found' % page_number)
    link.click()