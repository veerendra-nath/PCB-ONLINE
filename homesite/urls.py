from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeview ),
    path('contactus', views.homeview ),
    path('aboutus', views.homeview),
    path('rules', views.homeview),
]
