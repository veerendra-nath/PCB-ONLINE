from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^account/(?P<sub_path>(profile)|(addresses)|(password))/$',views.account_view,name='dashboard_account'),
]