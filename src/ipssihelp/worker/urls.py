from django.urls import path
from . import views

app_name = 'worker'

urlpatterns = [
    path('', views.home, name='home'),
    path('demand', views.demand, name='demand'),
    path('supply', views.supply, name='supply'),
    path('detail/<slug:slug>/', views.detail, name='detail'),
    path('account/signup/', views.signup, name='signup'),
    path('account/profile/<int:user_id>', views.worker_profile, name='signup'),
]
