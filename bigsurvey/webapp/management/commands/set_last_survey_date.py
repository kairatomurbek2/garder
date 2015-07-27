from django.core.management import BaseCommand
from webapp import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        for site in models.Site.objects.all():
            try:
                last_survey = site.surveys.latest('survey_date')
                site.last_survey_date = last_survey.survey_date
                site.save()
            except models.Survey.DoesNotExist:
                pass
