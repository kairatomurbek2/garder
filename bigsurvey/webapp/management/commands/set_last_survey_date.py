from django.core.management import BaseCommand
from webapp.models import Site


class Command(BaseCommand):
    def handle(self, *args, **options):
        for site in Site.objects.all():
            last_survey = site.surveys.latest('survey_date')
            site.last_survey_date = last_survey.survey_date
            site.save()
