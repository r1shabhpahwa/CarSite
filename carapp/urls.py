from django.urls import path
from . import views
from .views import LabMembersView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'carapp'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('<int:cartype_no>/', views.cardetail, name='cardetail'),
    path('lab_members/', LabMembersView.as_view(), name='lab_members'),
    path('carapp/<int:cartype_no>/', views.cardetail, name='cardetail'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('orderhere/', views.orderhere, name='order'),
    path('search/', views.search_vehicle, name='search'),
    path('accounts/login/', views.login_here, name='login'),
    path('accounts/logout/', views.logout_here, name='logout'),
    path('accounts/my_orders/', views.list_of_orders, name='my_orders'),
]
