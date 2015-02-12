from common_steps import *
from lettuce import *
from settings import *


@step('I open survey detail page with pk "(\d+)"')
def open_survey_detail_page(step, survey_pk):
    step.given('I open "%s"' % get_url(Urls.survey_detail % survey_pk))