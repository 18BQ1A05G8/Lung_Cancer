from django.conf import settings
# from django.conf.urls import url
# from django.contrib import admin
from django.urls import path,include
from . import views
from django.views.static import serve
urlpatterns = [
    path('',views.home,name='home'),
    path('results',views.results,name='results'), 
]