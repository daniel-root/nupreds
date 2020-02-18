from django.urls import path

from equipments import views

urlpatterns = [
    path('', views.equipment_list, name='equipment_list'),
    path('view/<int:pk>', views.equipment_view, name='equipment_view'),
    path('new', views.equipment_create, name='equipment_new'),
    path('edit/<int:pk>', views.equipment_update, name='equipment_edit'),
    path('delete/<int:pk>', views.equipment_delete, name='equipment_delete'),
]

'''urlpatterns = [
    path('', views.EquipmentList.as_view(), name='equipment_list'),
    path('view/<int:pk>', views.EquipmentView.as_view(), name='equipment_view'),
    path('new', views.EquipmentCreate.as_view(), name='equipment_new'),
    path('view/<int:pk>', views.EquipmentView.as_view(), name='equipment_view'),
    path('edit/<int:pk>', views.EquipmentUpdate.as_view(), name='equipment_edit'),
    path('delete/<int:pk>', views.EquipmentDelete.as_view(), name='equipment_delete'),
]'''