from django.urls import path

from . import views

urlpatterns = [
    path("category/", views.category_list_view, name="category_list"),
    path("category/<int:pk>/", views.category_detail_view, name="category_detail"),
    path("service/", views.service_list_view, name='service_list'),
    path('service/<int:pk>/', views.service_detail_view, name='service_detail'),
    path('staff/', views.staff_list_view, name='staff_list'),
    path('staff/<int:pk>/', views.staff_detail_view, name='staff_detail'),
    path('availablity/', views.availablity_list_view, name='availablity_list'),
    path('avaialablity/<int:pk>/', views.availablity_detail_view, name='availablity_detail'),
    path('slots/', views.slot_list_view, name='slots_list'),
    path('slots/<int:pk>/', views.slot_detail_view, name='slots_detail')



    # path("service/<int:pk>/", views.service_list_view, name="service_list"),
    # path("staff/<int:pk>/slots/", views.staff_list_view, name="staff_slots_list"),
    # path('appointment/', views.appointment_list_view, name='appointment_list'),
    # path('appointment/<int:pk>/', views.appointment_detail_view, name= 'appointment_detail'),
    # path('appointment/new/', views.appointment_create_view, name='create_appointment'),
]
