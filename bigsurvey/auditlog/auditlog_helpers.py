import json

import datetime

from diff_match_patch import diff_match_patch
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
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


def get_version_objects_with_diff(current_user_pws_list, **kwargs):
    start_date = kwargs.get('start_date')
    end_date = kwargs.get('end_date')
    pws = kwargs.get('pws')
    user_group = kwargs.get('user_group')
    username = kwargs.get('username')
    record_object = kwargs.get('record_object')

    range_end = end_date + datetime.timedelta(days=1)
    date_range = (start_date, range_end)

    pws_users = User.objects.filter(Q(employee__pws__in=current_user_pws_list) | Q(is_superuser=True))
    filtered_version_objects = Version.objects.filter(revision__date_created__range=date_range,
                                                      revision__user__in=pws_users)
    if pws:
        pws_list = [pws]
    else:
        pws_list = current_user_pws_list
    if user_group:
        if user_group.name == u'SuperAdministrators':
            filtered_version_objects = filtered_version_objects.filter(revision__user__is_superuser=True)
        else:
            users = User.objects.filter(groups=user_group, employee__pws__in=pws_list)
            filtered_version_objects = filtered_version_objects.filter(revision__user__in=users)
    if username:
        users = User.objects.filter(username__icontains=username)
        filtered_version_objects = filtered_version_objects.filter(revision__user__in=users)
    if record_object:
        filtered_version_objects = filtered_version_objects.filter(
            object_repr__icontains=record_object)
    filtered_version_objects = filtered_version_objects.order_by('-revision__date_created')
    target_objects = [(obj, render_diff(obj)) for obj in list(filtered_version_objects)
                      if _check_obj_pws(obj, pws_list) and len(render_diff(obj)) > 0]
    return target_objects


def _check_obj_pws(obj, pws_list):
    result = []
    if obj.content_type == ContentType.objects.get_for_model(User):
        if _user_belongs_to_one_of_the_user_pws(obj, pws_list):
            result.append(True)
    else:
        for pws in pws_list:
            try:
                if pws in obj.object.get_pws_list():
                    result.append(True)
                else:
                    result.append(False)
            except AttributeError:
                result.append(True)
    return True in result


def _user_belongs_to_one_of_the_user_pws(obj, pws_list):
    obj_pws_list = obj.object.employee.pws.all()
    common_pws_as_set = set(obj_pws_list).intersection(set(pws_list))
    return len(common_pws_as_set) > 0
