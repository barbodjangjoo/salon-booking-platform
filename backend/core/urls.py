from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', views.user_registration, name='user_register'),
    
    path('categories/', views.category_list_view, name='category_list'),
    path('service/<int:pk>/', views.services_detail_view, name='service_detail')
]