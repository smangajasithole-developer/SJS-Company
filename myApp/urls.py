from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    # =====================================================
    # 1. PUBLIC PAGES (Frontend)
    # =====================================================
    
    # Main Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('careers/', views.careers, name='careers'),
    path('contact/', views.contact, name='contact'),
    
    # Job Related
    path('job/<int:id>/', views.jobinfo, name='jobinfo'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
    
    
    # =====================================================
    # 2. AUTHENTICATION (Login, Register, Logout)
    # =====================================================
    
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    
    
    # =====================================================
    # 3. EMAIL VERIFICATION
    # =====================================================
    
    path("verify-email/<uuid:token>/", views.verify_email, name="verify_email"),
    path("resend-verification/", views.resend_verification_email, name="resend_verification"),
    
    
    # =====================================================
    # 4. PASSWORD RESET
    # =====================================================
    
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uuid:token>/', views.reset_password, name='reset_password'),
    
    
    # =====================================================
    # 5. USER DASHBOARD & PROFILE (Customer)
    # =====================================================
    
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path("delete-profile/", views.delete_profile, name="delete_profile"),
    
    # User Account Management
    path('notifications/', views.notifications, name='notifications'),
    path('inbox/', views.inbox, name='inbox'),
    path('settings/', views.settings, name='settings'),
    path('feedback/', views.feedback, name='feedback'),
    path('help/', views.help, name='help'),
    
    
    # =====================================================
    # 6. ADMIN DASHBOARD (Super Admin)
    # =====================================================
    
    # Main Admin
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('adminheader/', views.adminheader, name='adminheader'),
    path('adminusers/', views.adminusers, name='adminusers'),
    
    # Admin Page Content Management
    path('adminhome/', views.adminhome, name='adminhome'),
    path('adminabout/', views.adminabout, name='adminabout'),
    path('adminservices/', views.adminservices, name='adminservices'),
    path('admincareers/', views.admincareers, name='admincareers'),
    path('admincontact/', views.admincontact, name='admincontact'),
    path('adminfooter/', views.adminfooter, name='adminfooter'),
    
    # Admin Hero Photos
    path('adminherophotos/', views.adminherophotos, name='adminherophotos'),
    
    
    # =====================================================
    # 7. HR DASHBOARD (Human Resources)
    # =====================================================

    
    # HR Main Dashboard
    path('hrdashboard/', views.hrdashboard, name='hrdashboard'),
    
    # HR Recruitment Management
    path("hrapplicants/", views.hrapplicants, name="hrapplicants"),
    path("hrapplications/", views.hrapplications, name="hrapplications"),
    path("hrinterviews/", views.hrinterviews, name="hrinterviews"),
    path("hroffers/", views.hroffers, name="hroffers"),
    path("hrhired/", views.hrhired, name="hrhired"),
    
    # HR Job & Career Management
    path('hrcareers/', views.hrcareers, name='hrcareers'),
    path("hrjobs/", views.hrjobs, name="hrjobs"),
    
    # HR Reports
    path("hrreports/", views.hrreports, name="hrreports"),
    
    # HR Detailed Views
    path("hrapplicant-profile/<int:user_id>/", views.hrapplicant_profile, name="hrapplicant_profile"),
    path("hrapplicant_profile/", views.hrapplicant_profile, name="hrapplicant_profile"),
    path("hrapplication-view/<int:application_id>/", views.hrapplication_view, name="hrapplication_view"),




    path(
    "hraccepted_candidate/",
    views.hraccepted_candidate,
    name="hraccepted_candidate"
    ),

    path(
    "hrrejected_candidate/",
    views.hrrejected_candidate,
    name="hrrejected_candidate"
    ),

    path(
    "hrupdate-application-status/<int:application_id>/<str:status>/",
    views.hrupdate_application_status,
    name="hrupdate_application_status"
    ),


    path(
    "hrsend-candidate-admin/<int:application_id>/",
    views.hrsend_candidate_admin,
    name="hrsend_candidate_admin"
    ),


    path(
    "adminaccepted_candidate/",
    views.adminaccepted_candidate,
    name="adminaccepted_candidate"
    ),
    
    path(
    "adminapprove_application/<int:application_id>/",
    views.adminapprove_application,
    name="adminapprove_application"
    ),


     path(
    "adminapplication_view/<int:application_id>/",
    views.adminapplication_view,
    name="adminapplication_view"
    ),

    path(
    "adminapplication-view/<int:application_id>/",
    views.adminapplication_view,
    name="adminapplication_view"
    ),


    path(
    "delete-application/<int:application_id>/",
    views.delete_application,
    name="delete_application"
    ),



]

# =====================================================
# 8. MEDIA FILES (Development Only)
# =====================================================

if settings.DEBUG:urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

