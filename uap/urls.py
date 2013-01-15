from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'uap.views.home', name='home'),
    # url(r'^uap/', include('uap.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
    
    #REDIRECTS
    url(r'^no_access/$', 'uap_app.views.no_access' ),
    
    #BASIC
    #url(r'^tutee/upload_test/$', 'uap_app.views.upload_handler'),
    url(r'^$', 'uap_app.views.basecase_home' ),
    url(r'^tutee/signup/$', 'uap_app.views.basecase_signup_tutee' ),
    url(r'^coach/request/$', 'uap_app.views.basecase_coach_application' ),
    url(r'^tutee/agreement/$', 'uap_app.views.tutee_agreement' ),
    url(r'^tutee_agreement/$', 'uap_app.views.view_tutee_agreement' ),
    url(r'^contact/', 'uap_app.views.basecase_contact'),
    url(r'^tutee/signup/validate$', 'uap_app.views.tutee_signup' ),
    url(r'^accounts/login/$', 'uap_app.views.logging_in' ),
    url(r'^logout$', 'uap_app.views.logging_out' ),
    url(r'^login/pw_request/$', 'uap_app.views.pw_request' ),
    
    #TUTEE
    url(r'^tutee/ticket_(?P<pid>\d+)/cancel/$', 'uap_app.views.cancel_ticket' ),
    url(r'^tutee/ticket_(?P<pid>\d+)/confirm/$', 'uap_app.views.confirm_ticket' ),
    url(r'^tutee/ticket_(?P<pid>\d+)/reject/$', 'uap_app.views.reject_ticket' ),
    url(r'^tutee/new_ticket/$', 'uap_app.views.new_project' ),
    url(r'^tutee/profile/$', 'uap_app.views.tutee_profile' ),
    url(r'^tutee/home/$', 'uap_app.views.home_tutee' ),
    url(r'^home/failure$', 'uap_app.views.home_failure' ),
    url(r'^tutee/tickets/$', 'uap_app.views.all_requests_tutee' ),
    url(r'^tutee/ticket_(?P<pid>\d+)$', 'uap_app.views.project_tutee' ),
    url(r'^tutee/report/$', 'uap_app.views.report_tutee'),
    
    #COACH
    url(r'^coach/profile/$', 'uap_app.views.coach_profile' ),
    url(r'^coach/tickets/$', 'uap_app.views.all_requests_coach' ),
    url(r'^coach/home/$', 'uap_app.views.home_coach'),
    url(r'^coach/ticket_(?P<pid>\d+)$', 'uap_app.views.project_coach' ),
    url(r'^coach/ticket_(?P<pid>\d+)/withdraw/$', 'uap_app.views.coach_withdraw_ticket' ),
    url(r'^coach/submit_meeting_details/ticket_(?P<pid>\d+)$', 'uap_app.views.submit_mtg_details'),
    url(r'^coach/report/$', 'uap_app.views.report_coach'),
    
    #ADMIN
    url(r'^app_admin/home/$', 'uap_app.views.home_admin'),
    url(r'^app_admin/add_new/$', 'uap_app.views.add_new_admin'),
    url(r'^app_admin/coach_requests/$', 'uap_app.views.admin_coach_requests'),
    url(r'^app_admin/coach_request_(?P<pid>\d+)/accept/$', 'uap_app.views.add_coach'),
    url(r'^app_admin/coach_request_(?P<pid>\d+)/reject/$', 'uap_app.views.reject_coach_req'),
    url(r'^app_admin/project/details$', 'uap_app.views.project_details_admin' ),
    url(r'^app_admin/view_tickets/$', 'uap_app.views.admin_view_requests'),
    url(r'^app_admin/view_tutees/$', 'uap_app.views.admin_all_tutee'),
    url(r'^app_admin/view_coaches/$', 'uap_app.views.admin_all_coach'),
    url(r'^app_admin/view_coach(?P<pid>\d+)/$', 'uap_app.views.admin_view_coach'),
    url(r'^app_admin/view_coach(?P<pid>\d+)/hours/$', 'uap_app.views.view_coach_hours'),
    url(r'^app_admin/assign_request_(?P<pid>\d+)$', 'uap_app.views.assign_coach'),
    url(r'^app_admin/ticket_(?P<pid>\d+)$', 'uap_app.views.admin_view_request' ),
    url(r'^app_admin/ticket_(?P<pid>\d+)/assign/$', 'uap_app.views.assign_ticket' ),
    url(r'^app_admin/ticket_(?P<pid>\d+)/approve/$', 'uap_app.views.admin_approve_ticket' ),
    url(r'^app_admin/ticket_(?P<pid>\d+)/reject/$', 'uap_app.views.admin_reject_ticket' ),
    url(r'^app_admin/profile/$', 'uap_app.views.admin_profile' ),
    
    
    
   #   url(r'^pennypincher/$', 'pennypincher_test.views.home'),
#      url(r'^pennypincher/home/$', 'pennypincher_test.views.home'),
 #     url(r'^pennypincher/homer/$', 'pennypincher_test.views.homer'),
  #    url(r'^pennypincher/summary/$', 'pennypincher_test.views.summary'),
   #   url(r'^pennypincher/summary/(?P<detail_username>[a-zA-Z0-9]+)$', 'pennypincher_test.views.detail'), #test this page*****
    #  url(r'^pennypincher/settings$', 'pennypincher_test.views.settings'),
)
