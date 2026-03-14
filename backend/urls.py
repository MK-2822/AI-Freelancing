from django.contrib import admin
from django.urls import path, include
from .views import home_view, login_selection_view, auth_view, client_dashboard_view, freelancer_dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core_api.urls')),
    path('', home_view, name='home'),
    path('login', login_selection_view, name='frontend-login'),
    path('auth/<str:role>/<str:mode>', auth_view, name='auth'),
    path('client-dashboard', client_dashboard_view, name='client-dashboard'),
    path('freelancer-dashboard', freelancer_dashboard_view, name='freelancer-dashboard'),
]
