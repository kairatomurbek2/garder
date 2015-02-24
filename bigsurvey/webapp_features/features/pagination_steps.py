from common_steps import *
from lettuce import *
from selenium import *
from webapp.models import Site, Customer, PWS, CustomerCode
from main.parameters import STATES


TEST_SITES_COUNT = 100
TEST_CUSTOMERS_COUNT = 100


@step('I generate test sites')
def generate_test_sites(step):
    customer = Customer.objects.first()
    pws = PWS.objects.first()
    for i in xrange(0, TEST_SITES_COUNT):
        site = Site()
        site.customer = customer
        site.pws = pws
        site.address1 = 'TestAddress%s' % i
        site.city = 'TestCity%s' % i
        site.state = STATES[0][0]
        site.zip = 'TestZip%s' % i
        site.save()


@step('I delete test sites')
def delete_test_sites(step):
    Site.objects.filter(city__startswith='TestCity').delete()


@step('I generate test customers')
def generate_test_customers(step):
    code = CustomerCode.objects.first()
    for i in xrange(0, TEST_CUSTOMERS_COUNT):
        customer = Customer()
        customer.number = 'TestNumber%s' % i
        customer.name = 'TestName%s' % i
        customer.code = code
        customer.address1 = 'TestAddress%s' % i
        customer.city = 'TestCity%s' % i
        customer.state = STATES[0][0]
        customer.zip = 'TestZip%s' % i
        customer.save()


@step('I delete test customers')
def delete_test_customers(step):
    Customer.objects.filter(number__startswith='TestNumber').delete()


@step('I turn to the "(\d+)" page')
def click_pagination_link(step, page_number):
    link = helper.find(Xpath.Pattern.pagination_link % page_number)
    helper.check_element_exists(link, 'Pagination link with page number "%s" was not found' % page_number)
    link.click()