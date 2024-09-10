from django.urls import path
from . import views



urlpatterns =[
    path('profile/', views.userProfile, name="user-profile"),
    
    path('dashboard/<uuid:pk>/', views.dashboard, name="dashboard"),
    path('employeedirectory/', views.employeedirectory, name="employee-directory"),
    path('employeedetails/<uuid:pk>/', views.EmployeeDetails, name="employee-details"),

    path('employeeregistration/', views.EmployeeRegistration, name="employee-registration"),
    path('attendance/', views.attendancelist, name="attendance-list"),
    path('attendance/<uuid:pk>/', views.attendancedetail, name='attendance-detail'),                          
    path('attendance/checkin/', views.signAttendance, name="attendance-checkin"),
    path('leave-application/', views.leaveApplication, name='leave-application'),
    path('leave-status/', views.leaveStatus, name='leave-management'),
    path('leave-status/<int:leave_id>/', views.fullleaveStatus, name='view-leave'),
    path('assign-task/', views.create_task, name='assign-task'),
    path('assigned-task/', views.view_tasks, name='assigned-tasks'),
    path('task/<uuid:task_id>/', views.task_details, name='task-details'),

    path('login/', views.loginUser, name="login"),
    
    path('logout/', views.logoutUser, name="logout"),
    path('signup/', views.signupUser, name="signup"),
] 