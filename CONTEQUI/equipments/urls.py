from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from equipments import views

urlpatterns = [
    path('', views.home, name='home'),
    path('Equipamentos', views.equipment_list, name='equipment_list'),
    path('Emprestimo/<int:pk>', views.equipment_view, name='equipment_view'),
    path('Novo', views.equipment_create, name='equipment_new'),
    path('Editar/<int:pk>', views.equipment_update, name='equipment_edit'),
    path('InativarAtivar/<int:pk>', views.equipment_delete, name='equipment_delete'),
    path('Emprestar/<int:pk>', views.emprestar, name='emprestar'),
    path('Devolver/<int:pk>', views.devolver, name='devolver'),
    path('ConfirmarEmprestimo/<int:pk>', views.emprestar_user, name='emprestar_user'),
    path('ConfirmarDevolução/<int:pk>', views.devolver_user, name='devolver_user'),
    path('Filtro/<int:pk>', views.filter_list, name='filter_list'),
    path('Equipamentos/<str:value>', views.filter_type, name='filter_type'),
    path('Pesquisar', views.search, name='search'),
    path('reports_list', views.get_rastreio, name='reports_list'),
    path('reports_list2', views.get_rastreio_list, name='reports_list2'),
    path('reports_list3', views.get_rastreio_list2, name='reports_list3'),
    path('type_list', views.equipment_type_list, name='equipment_type_list'),
    path('type_view/<int:pk>', views.equipment_type_view, name='equipment_type_view'),
    path('type_new', views.equipment_type_create, name='equipment_type_new'),
    path('type_edit/<int:pk>', views.equipment_type_update, name='equipment_type_edit'),
    path('type_delete/<int:pk>', views.equipment_type_delete, name='equipment_type_delete'),
   
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)