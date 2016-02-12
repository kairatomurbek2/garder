from datetime import datetime
from lettuce import step
from webapp.models import PriceHistory
from webapp_features.features.data import Urls, get_url


@step('I open "price_setup" page')
def open_price_setup(step):
    step.given('I click "test_price" menu link')


@step('I directly open "price_setup" page')
def direct_open_price_setup(step):
     step.given('I open "%s"' % get_url(Urls.price_setup))


@step('Current default price started today')
def set_today_start_date_for_current_price(step):
    price = PriceHistory.current_for_test()
    price.start_date = datetime.now().date()
    price.save()
