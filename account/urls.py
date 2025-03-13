
from django.contrib.auth import views as auth_views 
from django.urls import include, path
from . import views
#added 2/11/25
from .views import patient_create_view, patient_list_view, patient_edit_view

urlpatterns = [
    
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change_form'),
    # path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),



    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    #added 2/11/25
    path('create-patient/', patient_create_view, name='create_patient'),
    path('my-patients/', patient_list_view, name='my_patients'),
    path('edit-patient/<int:patient_id>/', patient_edit_view, name='edit_patient'),
    # Add other URL patterns here
    path('select-drug/<int:patient_id>/', views.patient_select_drug_view, name='select_drug'),
   
    # path('patient/<int:patient_id>/', views.patient_doses_view, name='patient_doses'),
    path('select-patient-for-doses/', views.select_patient_for_doses_view, name='select_patient_for_doses'),
    path('patient/<int:patient_id>/doses/', views.patient_doses_view, name='patient_doses'),


]