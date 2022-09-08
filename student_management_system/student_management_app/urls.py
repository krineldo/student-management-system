from django.urls import path
from student_management_app import views


urlpatterns = [
    path('', views.login_page, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('register-as', views.register_as_page, name="register"),
    path('register-admin', views.admin_register_page, name="register-admin"),
    path('register-secretary', views.secretary_register_page, name="register-secretary"),
    path('register-student', views.student_register_page, name="register-student"),


    #Admin urls
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-announcement', views.admin_announcement_view, name='admin-announcement'),
    path('admin-view-secretary', views.admin_view_secretary_view, name='admin-view-secretary'),
    path('admin-approve-secretary', views.admin_approve_secretary_view, name='admin-approve-secretary'),
    path('approve-secretary/<int:pk>', views.approve_secretary_view, name='approve-secretary'),
    path('reject-secretary/<int:pk>', views.reject_secretary_view, name='reject-secretary'),
    path('admin-add-secretary', views.admin_add_secretary_view, name='admin-add-secretary'),
    path('update-secretary/<int:pk>', views.admin_update_secretary_view, name='update-secretary'),
    path('delete-secretary/<int:pk>', views.admin_delete_secretary_view, name='delete-secretary'),

    path('admin-view-student', views.admin_view_student_view, name='admin-view-student'),
    path('admin-approve-student', views.admin_approve_student_view, name='admin-approve-student'),
    path('approve-student/<int:pk>', views.approve_student_view, name='approve-student'),
    path('reject-student/<int:pk>', views.reject_student_view, name='reject-student'),
    path('admin-add-student', views.admin_add_student_view, name='admin-add-student'),
    path('update-student/<int:pk>', views.admin_update_student_view, name='update-student'),
    path('delete-student/<int:pk>', views.admin_delete_student_view, name='delete-student'),

    # Secretary urls
    path('secretary-dashboard', views.secretary_dashboard_view, name='secretary-dashboard'),
    path('secretary-announcement', views.secretary_announcement_view, name='secretary-announcement'),

    #Student urls
    path('student-dashboard', views.student_dashboard_view, name='student-dashboard'),
]
