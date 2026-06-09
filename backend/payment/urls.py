from django.urls import path

from . import views

urlpatterns = [
    path('factors/', views.factor_list_view, name='factor_list'),
    path('factors/<int:pk>/', views.factor_detail_view, name='factor_detail'),
]
