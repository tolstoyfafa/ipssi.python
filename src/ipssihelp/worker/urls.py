from django.urls import path, re_path
from . import views

app_name = 'worker'

urlpatterns = [
    path('', views.home, name='home'),
    path('demand', views.demand, name='demand'),
    path('supply', views.supply, name='supply'),
    path('detail/<slug:slug>/', views.detail, name='detail'),
    path('account/ads/', views.get_all_ads, name='ads'),
    path('account/signup/', views.signup, name='signup'),
    path('account/login/', views.login_worker, name='login'),
    path('account/logout/', views.logout_worker, name='logout'),
    path('account/profile/', views.worker_profile, name='profile'),
    path('account/contact/<slug:slug>/', views.contact, name='contact'),
    path('account/messages/', views.get_all_messages, name='messages'),
    path('account/convs/<slug:slug>/', views.get_all_convs, name='convs'),
    path('account/ads/ad_add', views.ad_add, name='ad_add'),
]
