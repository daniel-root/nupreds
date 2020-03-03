from django.urls import path


urlpatterns = [
   ''' path('', views.user_list, name='user_list'),
    path('view/<int:pk>', views.user_view, name='user_view'),
    path('new', views.user_create, name='user_new'),
    path('edit/<int:pk>', views.user_update, name='user_edit'),
    path('delete/<int:pk>', views.user_delete, name='user_delete'),'''
]
