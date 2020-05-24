from django.urls import path
from users import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('Previlegio/<int:pk>', views.user_view, name='user_view'),
    path('Novo', views.user_create, name='user_new'),
    path('Editar/<int:pk>', views.user_update, name='user_edit'),
    path('Inativar/<int:pk>', views.user_delete, name='user_delete'),
    path('TipoUsuario/<int:pk>', views.type_user, name='type_user'),
    path('Inativos/', views.user_list_inactive, name='user_list_inactive'),
]
