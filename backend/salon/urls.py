from django.urls import path

from . import views

urlpatterns = [
    path('category/', views.category_list_view, name='category_list'),
    path('category/<int:pk>/', views.category_detail_view, name='category_detail'),
    path('service/<int:pk>/', views.service_list_view, name='service_list'),
]
