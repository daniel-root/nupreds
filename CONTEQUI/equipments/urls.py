from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from equipments import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list', views.equipment_list, name='equipment_list'),
    path('view/<int:pk>', views.equipment_view, name='equipment_view'),
    path('new', views.equipment_create, name='equipment_new'),
    path('edit/<int:pk>', views.equipment_update, name='equipment_edit'),
    path('delete/<int:pk>', views.equipment_delete, name='equipment_delete'),
    path('emprestar<int:pk>', views.emprestar, name='emprestar'),
    path('devolver<int:pk>', views.devolver, name='devolver'),
    path('emprestar_user<int:pk>', views.emprestar_user, name='emprestar_user'),
    path('devolver_user<int:pk>', views.devolver_user, name='devolver_user'),
    path('filter_list<int:pk>', views.filter_list, name='filter_list'),
    path('filter_list/<str:value>', views.filter_type, name='filter_type'),
    path('search', views.search, name='search'),
    #path('reports_list', views.reports_list, name='reports_list'),
    path('reports_list', views.get_rastreio, name='reports_list'),
    path('reports_list2', views.get_rastreio_list, name='reports_list2'),
    path('reports_list3', views.get_rastreio_list2, name='reports_list3'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)