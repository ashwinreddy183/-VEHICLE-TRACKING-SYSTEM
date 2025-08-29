from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    #path('admin',views.admin,name="admin"),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('service_provider',views.service_provider,name='service_provider'),
    path('service_provider2',views.service_provider2,name='service_provider2'),
    path('update_coordinates', views.update_bus_coordinates, name='update_coordinates'),
    path('update_coordinates2', views.update_auto_coordinates, name='update_coordinates'),
    path('update_capacity', views.update_capacity, name='update_capacity'),
    path('update_bookings', views.update_bookings, name='update_bookings'),
    path('save_bus_info', views.save_bus_info, name='save_bus_info'),
    path('updater_page',views.updater_page,name='updater_page'),
    path('bus_info',views.bus_info,name='bus_info'),
    path('generate_map',views.generate_map,name='map'),
    path('generate_map2',views.generate_map2,name='map'),
    path('rickshaw_info',views.rickshaw_info,name='rickshaw_info'),
    path('service',views.service,name='service'),
    path('front_page',views.front_page,name='front'),
    path('end_trip',views.end_trip,name='end_trip'),
    path('signout2',views.signout2,name='auto_signout'),
    path('map',views.map,name='map'),
]