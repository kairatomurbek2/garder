from django.conf.urls import url, patterns
from accounts import views

urlpatterns = patterns('accounts.views',

    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),

)

