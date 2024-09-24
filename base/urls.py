from django.urls import path
from . import views


urlpatterns= [
    path('', views.landing, name='land'),
    path('home', views.home, name='home'),
    path('createstate', views.createState, name='createstate'),
    path('statecommittee', views.stateCommittee, name='statecommittee'),
    path('volunteer', views.volunteer, name='volunteer'),
    path('alerts', views.alerts, name='alerts'),
    path('AssignVoluenteersbyadmin/<str:pk>', views.AssignVoluenteersbyadmin, name='Assign_Voluenteers_byadmin'),
    
    path('needs', views.needs, name='needs'),
    
    path('addstate', views.addState, name='add-state'),
    path('addvolunteer', views.addVolunteer, name='add-volunteer'),
    path('createstate', views.createState, name='create-state'),
    path('editstate/<str:pk>', views.editState, name='edit-state'),
    path('editvolunteer/<str:pk>', views.editVolunteer, name='edit-volunteer'),
    path('edituser/<str:pk>', views.editEndUser, name='edit-user'),
   
    path('deletestate/<str:pk>', views.deleteState, name='delete-state'),
    path('deleteuser/<str:pk>', views.deleteUser, name='delete-user'),
    path('deletevolunteer/<str:pk>', views.deleteVolunteer, name='delete-volunteer'),
    path('volunteerhome', views.volunteerHome, name='volunteer-home'),
    path('userhome', views.userHome, name='user-home-temp'),
    path('login', views.loginPage, name='login'),
    path('register', views.register, name='register'),
    path('userregister', views.userRegister, name='user-register'),
    path('stateregister', views.stateRegister, name='state-register'),
    path('logout', views.logoutUser, name='logout'),

    path('needsverifybystate/<str:pk>', views.needsVerifyByState, name='needs-verify-by-state'),
    path('needsrejectbystate/<str:pk>', views.needsRejectByState, name='needs-reject-by-state'),

    path('closeneeds/<str:pk>', views.closeNeeds, name='close-needs'),
    path('deleteneeds/<str:pk>', views.deleteNeeds, name='delete-needs'),

    path('user/request/alert', views.userRequestPage, name='user-home'),

    path('approvealert/<str:pk>', views.verifyAlert, name='approve-alert'),
    path('rejectalert/<str:pk>', views.rejectAlert, name='reject-alert'),

    path('deletealert/<str:pk>', views.deleteAlert, name='delete-alert'),
    path('closealert/<str:pk>', views.closeAlert, name='close-alert'),

    path('mapalert/<str:pk>', views.mapAlert, name='map-alert'),
    path('unknownmapalert', views.unknownAlert, name='unknown-map-alert'),
    path('report/view', views.viewReports, name='view-report'),
    path('user/certificate/request', views.requestCertificate, name='request-certificate'),
    path('submit/request/certificate/<str:pk>', views.submitCertificate, name='submit-certificate'),
    path('certificate/view', views.viewCerficates, name='view-certificate'),
    path('certificate/approve/<str:pk>', views.approveCertificate, name='approve-certificate'),
    path('certificate/reject/<str:pk>', views.rejectCertificate, name='reject-certificate'),
    path('user/certificate/view/<str:pk>', views.fullCertificate, name='user-certificate-view'),
    path('weatherreport', views.weatherReport, name='weather-report'),
    path('hotspotview', views.hotspotView, name='hostspot-view'),
    path('save_alert', views.save_alert, name='save_alert'),
    path('viewtask/<str:id>', views.viewTask, name='viewtask'),
    path('viewallalers/', views.viewAllAlerts, name='viewallalerts'),
        # path('generate-pdf/', views.generate_pdf, name='generate_pdf'),

path('complaintsview', views.complaintsview, name='complaints_view'),
path('complaintsadd', views.complaintsadd, name='complaints_add'),
path('editcomplaint/<int:id>', views.editcomplaint, name='edit_complaint'),    
path('deletecomplaint/<int:id>', views.deletecomplaint, name='delete_complaint'),
path('estimateamount', views.estimateamount, name='estimate_amount'), 
path('viewestimateamount', views.viewestimateamount, name='view_estimateamount'), 
 path('approve/<int:estimate_id>', views.approve_estimate, name='approve_estimate'),
  path('reject/<int:estimate_id>', views.reject_estimate, name='reject_estimate'),
    path('claimuser', views.claimuser, name='claim_user'),
    path('viewclimuseradmin', views.viewclimuseradmin, name='view_climuseradmin'),
    path('viewtaskbystate', views.viewtaskebystate, name='view_task_by_state'),
    path('viewcomplaintsbyadmin', views.viewcomplaintsbyadmin, name='view_complaints_by_admin'),
    
    
    
 
]