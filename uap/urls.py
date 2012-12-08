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
    
    
    #TUTEE and BASIC
    url(r'^uap_app/$', 'uap_app.views.basecase_home' ),
    url(r'^uap_app/signup/$', 'uap_app.views.basecase_signup' ),
    url(r'^uap_app/tutee/signup/$', 'uap_app.views.basecase_signup_tutee' ),
   # url(r'^uap_app/signup/coach/$', 'uap_app.views.basecase_signup_coach' ),
    url(r'^uap_app/tutee/agreement/$', 'uap_app.views.tutee_agreement' ),
    url(r'^uap_app/tutee/signup/validate$', 'uap_app.views.tutee_signup' ),
    
   
    
    url(r'^uap_app/tutee/new_request/$', 'uap_app.views.new_project' ),
    url(r'^uap_app/tutee/profile/$', 'uap_app.views.tutee_profile' ),
    url(r'^uap_app/tutee/home/success$', 'uap_app.views.home_success_tutee' ),
    url(r'^uap_app/tutee/home/$', 'uap_app.views.home_tutee' ),
    url(r'^accounts/login/home/success$', 'uap_app.views.home_success' ),
    url(r'^uap_app/home/failure$', 'uap_app.views.home_failure' ),
    url(r'^accounts/login/$', 'uap_app.views.logging_in' ),
    url(r'^uap_app/admin/project/details$', 'uap_app.views.project_details_admin' ),
    url(r'^uap_app/logout$', 'uap_app.views.logging_out' ),
    url(r'^uap_app/tutee/requests/$', 'uap_app.views.all_requests_tutee' ),
    url(r'^uap_app/tutee/request_(?P<pid>\d+)$', 'uap_app.views.project_tutee' ),
    url(r'^uap_app/tutee/report/$', 'uap_app.views.report_tutee'),
    
    #COACH
    url(r'^uap_app/coach/profile/$', 'uap_app.views.coach_profile' ),
    url(r'^uap_app/coach/requests/$', 'uap_app.views.all_requests_coach' ),
    url(r'^uap_app/coach/home/$', 'uap_app.views.home_coach'),
    url(r'^uap_app/coach/request_(?P<pid>\d+)$', 'uap_app.views.project_coach' ),
    url(r'^uap_app/coach/submit_meeting_details/request_(?P<pid>\d+)$', 'uap_app.views.submit_mtg_details'),
    url(r'^uap_app/coach/report/$', 'uap_app.views.report_coach'),
    
    #ADMIN
    url(r'^uap_app/admin/home/$', 'uap_app.views.home_admin'),
    url(r'^uap_app/admin/view_requests/$', 'uap_app.views.admin_view_requests'),
    url(r'^uap_app/admin/view_tutee/$', 'uap_app.views.admin_all_tutee'),
    url(r'^uap_app/admin/view_coach/$', 'uap_app.views.admin_all_coach'),
    url(r'^uap_app/admin/assign_request_(?P<pid>\d+)$', 'uap_app.views.assign_coach'),
    url(r'^uap_app/admin/request_(?P<pid>\d+)$', 'uap_app.views.admin_view_request' ),
    url(r'^uap_app/admin/profile/$', 'uap_app.views.admin_profile' ),
    
    
    
   #   url(r'^pennypincher/$', 'pennypincher_test.views.home'),
#      url(r'^pennypincher/home/$', 'pennypincher_test.views.home'),
 #     url(r'^pennypincher/homer/$', 'pennypincher_test.views.homer'),
  #    url(r'^pennypincher/summary/$', 'pennypincher_test.views.summary'),
   #   url(r'^pennypincher/summary/(?P<detail_username>[a-zA-Z0-9]+)$', 'pennypincher_test.views.detail'), #test this page*****
    #  url(r'^pennypincher/settings$', 'pennypincher_test.views.settings'),
)
