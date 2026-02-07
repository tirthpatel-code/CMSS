from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('complaints/', views.complaints_list, name='complaints_list'),
    path('complaint/create/', views.create_complaint, name='create_complaint'),
    path('complaint/<str:ticket_number>/', views.complaint_detail, name='complaint_detail'),
    path('api/complaints/', views.api_complaints, name='api_complaints'),
    path('api/stats/', views.api_stats, name='api_stats'),
    path('api/complaint/<str:ticket_number>/status/', views.update_complaint_status, name='update_status'),
    path('api/complaint/<str:ticket_number>/assign/', views.assign_complaint, name='assign_complaint'),
    path('api/complaint/<str:ticket_number>/comment/', views.add_comment, name='add_comment'),
]
