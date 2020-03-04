from django.urls import path
from .views import HomePageView

from equipments import views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('alist', views.equipment_list, name='equipment_list'),
    path('aview/<int:pk>', views.equipment_view, name='equipment_view'),
    path('anew', views.equipment_create, name='equipment_new'),
    path('aedit/<int:pk>', views.equipment_update, name='equipment_edit'),
    path('adelete/<int:pk>', views.equipment_delete, name='equipment_delete'),
    path('list', views.client_list, name='client_list'),
    path('view/<int:pk>', views.client_view, name='client_view'),
    path('new', views.client_create, name='client_new'),
    path('edit/<int:pk>', views.client_update, name='client_edit'),
    path('delete/<int:pk>', views.client_delete, name='client_delete'),
    path('tlist', views.equipment_type_list, name='equipment_type_list'),
    path('tview/<int:pk>', views.equipment_type_view, name='equipment_type_view'),
    path('tnew', views.equipment_type_create, name='equipment_type_new'),
    path('tedit/<int:pk>', views.equipment_type_update, name='equipment_type_edit'),
    path('tdelete/<int:pk>', views.equipment_type_delete, name='equipment_type_delete'),
]
