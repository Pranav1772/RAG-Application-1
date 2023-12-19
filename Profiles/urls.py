from django.urls import path, include
from Profiles import views

urlpatterns = [
    path("admin_dashboard/",views.dashboard,name='dashboard'),
    path("manage_docs/",views.manage_docs,name='manage_docs'),
    path("manage_users/",views.manage_users,name='manage_users'),
    path("add_user/",views.add_user,name='add_user'),
    path("upload_pdf/",views.upload_pdf,name='upload_pdf'),
    path('update_user/<int:user_id>/', views.update_user, name='update_user'),
    # path('update_users_page/', views.update_users_page, name='update_users_page'),
    path('update_activity/', views.update_activity, name='update_activity'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('delete_pdf/<int:pdf_id>/', views.delete_pdf, name='delete_pdf'),
]
