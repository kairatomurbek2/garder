from django import template
import git
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_git_tag_and_date():
    repo = git.Repo(settings.BASE_DIR + "/../.git")
    describe = repo.git.describe('--tags', '--abbrev=0')
    return "v" + describe