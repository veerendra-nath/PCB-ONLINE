from django.urls import path,re_path
from . import views

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('login/redir=<path:redir>',views.login_view,name='login_redir'),
    path('create/',views.create_view,name='create'),
    path('create/redir=<path:redir>',views.create_view,name='create'),
    path('logout/',views.logout_view,name='logout'),
]