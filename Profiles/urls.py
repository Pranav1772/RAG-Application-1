from django.urls import path, include
from Profiles import views

urlpatterns = [
    path("admin_dashboard/",views.dashboard,name='dashboard'),
    path("manage_docs/",views.manage_docs,name='manage_docs'),
    path("manage_users/",views.manage_users,name='manage_users'),
    path("add_user/",views.add_user,name='add_user'),
    path("upload_pdf/",views.upload_pdf,name='upload_pdf'),
    path('update_user/<int:user_id>/', views.update_user, name='update_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('delete_pdf/<int:user_id>/', views.delete_pdf, name='delete_pdf'),
    path('reprocess_pdf/<int:user_id>/', views.reprocess_pdf, name='reprocess_pdf'),
]
