
import json

from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from diff_match_patch import diff_match_patch
from reversion.models import Version

dmp = diff_match_patch()
SEMANTIC = 1
EFFICIENCY = 2


def render_diff(obj):
    result = ""
    try:
        diff = _get_diff_from_objects(obj)
        for key in diff:
            result += "<p>%s</p>" % key
            result += "<p>" + _html_diff(diff[key]['prev'], diff[key]['current'], EFFICIENCY) + "</p>"
    except IndexError:
        result = ""
    except ValueError:
        result = ""
    return result


def _html_diff(value1, value2, cleanup=SEMANTIC):
    """
    Generates a diff used google-diff-match-patch

    The cleanup parameter can be SEMANTIC, EFFICIENCY or None to clean up the diff
    for greater human readibility.
    """
    value1 = force_unicode(value1)
    value2 = force_unicode(value2)
    # Generate the diff with google-diff-match-patch
    diff = dmp.diff_main(value1, value2)
    if cleanup == SEMANTIC:
        dmp.diff_cleanupSemantic(diff)
    elif cleanup == EFFICIENCY:
        dmp.diff_cleanupEfficiency(diff)
    elif cleanup is not None:
        raise ValueError("cleanup parameter should be one of SEMANTIC, EFFICIENCY or None.")
    html = dmp.diff_prettyHtml(diff)
    html = html.replace("&para;<br>", "</br>")

    html = mark_safe(html)
    return html


def _get_diff_from_objects(obj):
    prev_objects = Version.objects.filter(object_id_int=obj.object_id_int,
                                          content_type=obj.content_type,
                                          revision__date_created__lt=obj.revision.date_created
                                          ).order_by('-revision__date_created')
    if len(prev_objects) > 0:
        prev_obj = prev_objects[0]
        prev_version = json.loads(prev_obj.serialized_data)
        current_version = json.loads(obj.serialized_data)
        diff = _compare_objects(current_version[0]['fields'], prev_version[0]['fields'])
        return diff
    return {}


def _compare_objects(current_version, prev_version):
    result = {}
    for key in current_version:
        if prev_version.has_key(key) and current_version[key] != prev_version[key]:
            result[key] = {}
            result[key]['current'] = current_version[key]
            result[key]['prev'] = prev_version[key]
    return result

