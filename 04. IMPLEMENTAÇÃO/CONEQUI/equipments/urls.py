from django.urls import path
from equipments import views

urlpatterns = [
    path('', views.home, name='home'),
    path('Equipamentos', views.equipment_list, name='equipment_list'),
    path('Emprestimo/<int:pk>', views.equipment_view, name='equipment_view'),
    path('Email/<int:pk>', views.email_, name='email_'),
    path('Novo', views.equipment_create, name='equipment_new'),
    path('Editar/<int:pk>', views.equipment_update, name='equipment_edit'),
    path('InativarAtivar/<int:pk>', views.equipment_delete, name='equipment_delete'),
    path('Emprestar/<int:pk>', views.emprestar, name='emprestar'),
    path('Devolver/<int:pk>', views.devolver, name='devolver'),
    path('ConfirmarEmprestimo/<int:pk>', views.emprestar_user, name='emprestar_user'),
    path('ConfirmarDevolução/<int:pk>', views.devolver_user, name='devolver_user'),
    path('Filtro/<str:pk>/<str:value>', views.filter_list, name='filter_list_equipment'),
    path('Filtro/<str:value>', views.filter_type, name='filter_type_equipment'),
    path('Pesquisar/<str:value>/<str:search_>', views.search, name='search'),
    path('Tipo/Pesquisar', views.search_type, name='search_type'),
    path('Relatórios/<str:value>', views.get_rastreio, name='get_rastreio'),
    path('Tipo', views.equipment_type_list, name='equipment_type_list'),
    path('Tipo/Ver/<int:pk>', views.equipment_type_view, name='equipment_type_view'),
    path('Tipo/Novo', views.equipment_type_create, name='equipment_type_new'),
    path('Tipo/Editar/<int:pk>', views.equipment_type_update, name='equipment_type_edit'),
    path('Tipo/Inativar/<int:pk>', views.equipment_type_delete, name='equipment_type_delete'),
    path('Inativos/<str:value>', views.equipment_list_inactive, name='equipment_list_inactive'),
    path('Tipo/<str:value>', views.equipment_type_order_by, name='equipment_type_order_by'),
    path('Listagem/<str:order_by>/<str:type_equipment_>', views.listagem, name='listagem'),
    path('Rastreio/<str:order_by>/<str:type_equipment_>/<str:tag>/<str:start>/<str:end>', views.rastreio, name='rastreio'),
    path('NaoDevolvidos/<str:order_by>/<str:type_equipment_>/<str:tag>/<str:start>', views.nao_devolvidos, name='nao_devolvidos'),
    path('GerarPDF/<str:report>/<str:type_equipment>/<str:tag>/<str:start>/<str:end>/<str:order_by>', views.some_view, name='some_view'),
   
]