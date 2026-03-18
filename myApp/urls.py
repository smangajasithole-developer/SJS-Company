from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('careers/', views.careers, name='careers'),
    path('contact/', views.contact, name='contact'),

    path('profile/', views.profile, name='profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('inbox/', views.inbox, name='inbox'),
    path('settings/', views.settings, name='settings'),
    path('feedback/', views.feedback, name='feedback'),
    path('help/', views.help, name='help'),

    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('hrsignin/', views.hrsignin, name='hrsignin'),

    path('apply/', views.apply, name='apply'),
    
]
