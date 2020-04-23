from django.urls import path
from . import views

app_name = 'worker'

urlpatterns = [
    path('', views.home, name='home'),
    path('demand', views.demand, name='demand'),
    path('supply', views.supply, name='supply'),
    path('detail/<slug:slug>/', views.detail, name='detail'),
    path('account/ads/', views.getAllAds, name='ads'),
    path('account/signup/', views.signup, name='signup'),
    path('account/login/', views.login_worker, name='login'),
    path('account/profile/', views.worker_profile, name='profile'),
]
