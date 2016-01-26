from webapp import models


def get_user_pws_list(request):
    pws_list = models.PWS.objects.none()
    if request.user.has_perm('webapp.browse_all_pws'):
        pws_list = models.PWS.objects.all()
    elif request.user.has_perm('webapp.own_multiple_pws'):
        pws_list = request.user.employee.pws.all()
    return pws_list
