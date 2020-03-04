from django.urls import path
from .views import HomePageView

from equipments import views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('list', views.equipment_list, name='equipment_list'),
    path('view/<int:pk>', views.equipment_view, name='equipment_view'),
    path('new', views.equipment_create, name='equipment_new'),
    path('edit/<int:pk>', views.equipment_update, name='equipment_edit'),
    path('delete/<int:pk>', views.equipment_delete, name='equipment_delete'),
]
