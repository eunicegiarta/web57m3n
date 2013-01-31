from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from uap_app.models import *
from uap_app.populate_db import *
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpRequest
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib import messages
import datetime 
import json
import math
from decimal import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse

def upload_handler(request):
    view_url = reverse('upload_handler')
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        form.save()
        return HttpResponseRedirect(view_url)

    upload_url, upload_data = prepare_upload(request, view_url)
    form = UploadForm()
    return direct_to_template(request, 'upload/upload.html',
        {'form': form, 'upload_url': upload_url, 'upload_data': upload_data})

@login_required
def no_access(request):
    # users should be one of three types: ADMIN, TUTEE, COACH
    if request.user.groups.filter(name="tutee").exists():
        return HttpResponseRedirect('/tutee/home/')
    elif request.user.groups.filter(name="coach").exists():
        return HttpResponseRedirect('/coach/home/')
    elif request.user.is_superuser:
        return HttpResponseRedirect('/app_admin/home/')
    else:
        return HttpResponseRedirect('/logout')

def basecase_home(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/app_admin/home/')
    form = TuteeUserForm()
    return render_to_response('home.html', {'form': form}, context_instance=RequestContext(request))

def basecase_coach_application(request):
    if request.method == 'POST':
        form = CoachReqForm(request.POST)
        if form.is_valid():
            n = CoachRequest()
            n.athena = request.POST['athena_username']
            n.first_name = request.POST['first_name'] 
            n.last_name = request.POST['last_name']
            n.email = request.POST['athena_username']+'@mit.edu'
            n.phone = request.POST['phone']
            n.uat_semester = request.POST['uat_semester']
            n.uat_year =request.POST['uat_year']
            n.course =request.POST['course']
            n.save()
            messages.success(request, 'Application successfully submitted.  Thank you for your interest in becoming a coach with CSCC.  We will be in contact with you shortly!')
            # email prospective coach
            email = EmailMessage('[CSCC] Thank you for applying to be a Coach!', 'Hi '+n.first_name+'! \n \nThank you for your interest in CSCC!  Your Coach application has been received and will be reviewed.  A decision should be made shortly. \n\nAll the best,\nThe CSCC Team\n\n\nDo not respond to this email as it is unmoderated.  Use the REPORT page to contact us.', to=[n.email])
            email.send()
            # email notification to ADMIN users
            admin_emails = get_admin_emails()
            email = EmailMessage('[CSCC Action Required] New Coach Request', 'A new Coach Request has been submitted and needs review.\n \nCSCC Auto-Notifications', to=admin_emails)
            email.send()
            
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'NOTE: Your coach application was not submitted properly.  Please try again!')
            return HttpResponseRedirect('/coach/request/')
                
        return render_to_response('coach_application.html', {'form': form, 'user': request.user }, context_instance=RequestContext(request)) #CHANGE THIS 
    form = CoachReqForm()
    return render_to_response('coach_application.html', {'form': form}, context_instance=RequestContext(request))

# helper function that returns a list of ADMIN user email address strings
def get_admin_emails():
    admin_users = User.objects.filter(is_superuser = True)
    emails = [str(each.email) for each in list(admin_users)]
    return emails

def basecase_signup(request):
    return render_to_response('signup.html', context_instance=RequestContext(request))
    
def basecase_signup_tutee(request):
    if request.method == 'POST':
        form = TuteeUserForm(request.POST)
        if form.is_valid():
            
            u = User.objects.create_user(username = request.POST['username'], password=request.POST['password'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'])
            u.groups.add(Group.objects.get(name='tutee'))
            u.save()
            t = TuteeUser()
            t.user = u
            t.phone = request.POST['phone']
            t.research_advisor_email = request.POST['research_advisor_email']
            t.open_project = False
            t.save()
            messages.success(request, 'You have successfully signed up!  Please login to your account')
            return HttpResponseRedirect("/accounts/login/")
    else:
        form = TuteeUserForm()
    return render_to_response('tutee_signup.html', {'form':form}, context_instance=RequestContext(request))

def tutee_signup(request):
    if request.method == "POST":
        form = ValidateAgreementForm(request.POST)
        if form.is_valid():
            d = request.session['tutee_signup']
            tu = User.objects.create_user(username = str(d['username']), password=str(d['password']))
            tu.first_name = str(d['first_name']) 
            tu.last_name = str(d['last_name'])
            tu.email = str(d['username'])+'@mit.edu'
            tu.groups.add(Group.objects.get(name='tutee'))
            tu.save()
            ttu = TuteeUser()
            ttu.user = tu
            '''
            try: 
                d['ee_request']         #check if TUTEE indicated EE-related
                ttu.ee_request = True
            except:
                ttu.ee_request = False
            try:
                d['cs_request']         #check if TUTEE indicated CS-related
                ttu.cs_request = True
            except:
                ttu.cs_request = False
            '''
            ttu.open_project = False
            ttu.research_advisor_email = str(d['research_advisor_email'])
            ttu.phone = str(d['phone'])
            ttu.save()
            messages.success(request, 'You have successfully signed up!  Please login to your account')
            email = EmailMessage('[CSCC] Welcome, '+tu.first_name+'!', 'Hi '+tu.first_name+'! \n \nWelcome to CSCC.  You have successfully signed up as a Tutee!  Log in to open a new ticket and get matched with a personal Coach. \n \nusername: '+tu.username+'\npassword: '+str(d['password'])+'\n\nThanks,\nThe CSCC Team\n\n\nDo not respond to this email as it is unmoderated.  Use the REPORT page to contact us.', to=[tu.email])
            email.send()
            return HttpResponseRedirect("/accounts/login/")
        else:
            messages.error(request, "NOTE: You must acknowledge and agree with the terms below to continue.")
            return render_to_response('agreement.html', {'form':form}, context_instance=RequestContext(request))
    else:
        return render_to_response('agreement.html', {'form':form}, context_instance=RequestContext(request))    
    
def tutee_agreement(request):
    test = False
    new_user_data = request.POST
    if request.method=='POST':
        form = TuteeUserForm(request.POST)
        if form.is_valid():
            try: 
                User.objects.get(username=str(request.POST['username']))
                test = True
            except:
                test = False
            if test:
                form = TuteeUserForm(initial=new_user_data)
                messages.success(request, 'NOTE: The username '+str(request.POST['username'])+' has been taken.  Please select a new username.')
                return render_to_response('tutee_signup.html', {'form':form}, context_instance=RequestContext(request))
            request.session['tutee_signup'] = request.POST
        else:
            try: 
                User.objects.get(username=str(request.POST['username']))
                test = True
            except:
                test = False
            if test:
                form = TuteeUserForm(initial=new_user_data)
                messages.success(request, 'NOTE: The username '+str(request.POST['username'])+' has been taken.  Please select a new username.')
                return render_to_response('tutee_signup.html', {'form':form}, context_instance=RequestContext(request))
            return render_to_response('tutee_signup.html', {'form':form}, context_instance=RequestContext(request))
    form = ValidateAgreementForm()
    return render_to_response('agreement.html', {'form':form, 'new_user_data':new_user_data}, context_instance=RequestContext(request))    

@login_required    
def view_tutee_agreement(request):
    if not request.user.groups.filter(name="tutee").exists():
        return HttpResponseRedirect('/no_access/')
    return render_to_response('view_agreement.html', context_instance = RequestContext(request))

def logging_in(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return HttpResponseRedirect('/app_admin/home')
                elif user.groups.filter(name="tutee").exists():
                    return HttpResponseRedirect('/tutee/home/')
                elif user.groups.filter(name="coach").exists():
                    return HttpResponseRedirect('/coach/home/')
                else:    
                    messages.error(request, 'Login was unsuccessful. Try again, or sign up to start!')
                    return HttpResponseRedirect('/accounts/login/')         
        else:
                messages.error(request, 'Login information is incorrect')
                return HttpResponseRedirect('/accounts/login/')
    return render_to_response('login.html', context_instance=RequestContext(request))

def logging_out(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out; please come back soon!')
    return render_to_response('login.html', context_instance=RequestContext(request))

def pw_request(request):
    if request.method=='POST':
        if User.objects.filter(username=request.POST['username']).exists():
            u = User.objects.get(username=request.POST['username'])
            password = User.objects.make_random_password()
            u.set_password = password
            u.save()
            email = EmailMessage('[CSCC] Password Reset', 'You have requested a new password. \n\n'+password+'\n\nPlease login with this new password and change it from the PROFILE page. \n\nThanks,\nThe CSCC Team\n\n\nDo not respond to this email as it is unmoderated.  Use the REPORT page to contact us.', to=[u.email])
            email.send()
            messages.success(request,"Your password has been reset and an email will be sent to you shortly.")
        else:
            messages.error(request,"We cannot find that username in our system.  Please sign up for CSCC!")
        return HttpResponseRedirect('/accounts/login/')
    return render_to_response('new_password.html', {'request': request}, context_instance=RequestContext(request))

def admin_logout(request):
    return HttpResponseRedirect('/logout/')

def basecase_contact(request):
    if request.method=="POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            admin_email = get_admin_emails()
            email = EmailMessage('[CSCC CONTACT FORM] '+request.POST['subject'], 'SENT FROM: '+str(request.POST['name'])+', EMAIL: '+ str(request.POST['email'])+'\n\n'+request.POST['message'], to=admin_email)
            email.send()
            messages.success(request, 'Your message to CSCC has been sent')
            return HttpResponseRedirect("/")
    form = ContactForm()
    return render_to_response('contact.html', {'form': form}, context_instance=RequestContext(request))
    
"""
A TuteeUser opens a new project; new project is created IF no open projects
"""    
@login_required
def new_project(request):
    if not request.user.groups.filter(name="tutee").exists():
        return HttpResponseRedirect('/no_access/')
    curruser = request.user.tuteeuser
    if request.method == 'POST':
        form = TicketForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            if curruser.open_project == False:
                t = Ticket()
                t.title = form.data['title']
                t.description = form.data['details']
                t.status = 'NAS'
                t.tutee = curruser
                t.date_of_interest = form.data['date_of_interest']
                t.area_of_interest = form.data['area_of_interest']
                t.save()
                curruser.open_project = True
                curruser.save()
                messages.success(request, 'You have successfully created a new Ticket')
                # email notification to ADMIN users
                admin_emails = get_admin_emails()
                email = EmailMessage('[CSCC Action Required] New Ticket', 'A new Ticket has been created and needs a Coaching assignment.\n \nCSCC Auto-Notifications', to=admin_emails)
                email.send()
                return HttpResponseRedirect('/tutee/home/')
            else:
                return render_to_response('homebase.html', context_instance=RequestContext(request))
                
        return render_to_response('new_project.html', {'form': form, 'user': request.user }, context_instance=RequestContext(request)) #CHANGE THIS 
    
    form = TicketForm()
    return render_to_response('new_project.html', {'form': form}, context_instance=RequestContext(request))

@login_required    
def home_tutee(request):
    if not request.user.groups.filter(name="tutee").exists():
        return HttpResponseRedirect('/no_access/')
    new = [1]       # hack: to check if tutee has open project
    tickets = []
    current = None
    confirm =False
    if request.user.tuteeuser.open_project:
        #if request.user.tuteeuser.get(user = request.user) == None:
         #   print "NONE"
        new.remove(1)
        tickets = list(request.user.tuteeuser.ticket_set.all())
        for each in tickets:
            if each.status == 'NAS' or each.status=='CAS' or each.status=='CSB':
                current = each
                if current.status == 'CSB':
                    confirm=True
    return render_to_response('homebase.html', {'request':request, 'current': current, 'new': new, 'confirm':confirm}, context_instance=RequestContext(request))
    
@login_required    
def home_coach(request):
    if not request.user.groups.filter(name="coach").exists():
        return HttpResponseRedirect('/no_access/')
        
    open_tix = Ticket.objects.filter(coach=request.user.coachuser).filter(status='CAS')
    return render_to_response('home_coach.html', {'request':request, 'open_tix':open_tix}, context_instance=RequestContext(request))
    
@login_required    
def home_admin(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/no_access/')
    req = list(CoachRequest.objects.filter(status='OP'))
    to_assign = list(Ticket.objects.filter(status='NAS'))
    to_review = list(Ticket.objects.filter(status='TCF'))
    num_no = len(req) + len(to_assign) + len(to_review)
    return render_to_response('home_admin.html', {'request':request, 'req':req, 'to_assign':to_assign, 'to_review':to_review, 'num_no': num_no}, context_instance=RequestContext(request))

def home_failure(request):
    print "********"+ request.user.username + " is logged in"
    messages.info(request, 'INFO')
    messages.error(request, 'ERROR')
    return render_to_response('homebase.html', context_instance=RequestContext(request))

def create_coach(request):
    if request.method == 'POST':
        return
    return HttpResponseRedirect('project_details.html', {'p': p})
        

# manipulate the details and add a note
@login_required
def project_details_admin(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/no_access/')
    p = Project.objects.get(id=1)
    return render_to_response('project_details.html', {'p': p}, context_instance=RequestContext(request))


@login_required
def all_requests_tutee(request):
    if not request.user.groups.filter(name="tutee").exists():
        return HttpResponseRedirect('/no_access/')
    u = request.user
    t = u.tuteeuser
    past_tix = list(t.ticket_set.all())
    curr = []
    cancelled=[]
    create = [1]

    for each in past_tix:
        if each.status =='CNL':
            cancelled.append(each)
            past_tix.remove(each)

    if t.open_project:
        create.remove(1)
        for each in past_tix:
            if each.status != 'TCF' and each.status != 'APR' and each.status != 'CNL' and each.status !='NAP':
                curr.append(each)
                past_tix.remove(each)
                break

    return render_to_response('all_projects_tutee.html', {'u': u, 't':t, 'cancelled': cancelled, 'projects':past_tix, 'curr':curr, 'create': create}, context_instance=RequestContext(request)) 
    
        
@login_required
def all_requests_coach(request):
    if not request.user.groups.filter(name="coach").exists():
        return HttpResponseRedirect('/no_access/')
    u = request.user
    c = u.coachuser
    prev_tix = list(c.ticket_set.all())
    open_tix = []
    pending = []
    for each in prev_tix:
        if each.status == 'CAS':
            open_tix.append(each)
            prev_tix.remove(each)
        elif each.status == 'CSB' or each.status=='TCF':
            pending.append(each)
            prev_tix.remove(each)
        elif each.status =='CNL':
            prev_tix.remove(each)
    
    
        # this leaves 'APR' and 'NAP' 
    return render_to_response('all_projects_coach.html', {'u': u, 'c':c, 'past':prev_tix, 'open':open_tix, 'pending': pending}, context_instance=RequestContext(request)) 

@login_required    
def project_tutee(request, pid = "nope"):
    if not request.user.groups.filter(name="tutee").exists():
        return HttpResponseRedirect('/no_access/')
    if pid.isdigit() == False:
        return HttpResponseRedirect('/no_access/')
    confirm = []
    details = []
    cancellable=False
    p = Ticket.objects.get(id = int(pid))
    tix_details = None
    try:
        tix_details = TicketDetails.objects.get(ticket=p)
    except:
        None
    vid = None
    try:
        vid = TicketVideoURL.objects.get(ticket=p)
    except:
        try:
            vid = TicketVideo.objects.get(ticket=p)
        except:
            None
    # ensures that this ticket originated from the tutee requesting details
    if p.tutee.user != request.user:
        return HttpResponseRedirect('/no_access/')
    if p.status == 'NAS':
        stat = "waiting for coach assignment"
        cancellable=True
    elif p.status == 'CAS':
        stat = "coach assigned, waiting for meeting details"
        cancellable=True
    elif p.status == 'CSB':
        stat = "meeting details completed, waiting for your confirmation of meeting"
        details.append(1)
        confirm.append(1)
    elif p.status =='TCF' or p.status =='APR' or p.status=='NAP':
        stat ="meeting complete, request closed"
        details.append(1)
    elif p.status=='CNL':
        stat="request was cancelled"
    else:
        stat="UNKNOWN--contact administrator"
    return render_to_response('tutee_project.html', {'p':p, 'cancellable':cancellable, 'stat': stat, 'confirm':confirm, 'details':details, 'vid':vid, 'tix_details':tix_details}, context_instance = RequestContext(request))
   
@login_required
def cancel_ticket(request, pid="no"):
    if not request.user.groups.filter(name="tutee").exists():
        return HttpResponseRedirect('/no_access/')
    if pid.isdigit()==False:
        return render_to_response('/tutee/home')
    t = Ticket.objects.get(id=int(pid))
    # ensures that this ticket originated from the tutee requesting details
    if t.tutee.user != request.user:
        return HttpResponseRedirect('/no_access/')
    if t.status == 'NAS' or t.status == 'CAS':
        request.user.tuteeuser.open_project = False
        request.user.tuteeuser.save()
        if t.status =='CAS':
            t.coach.projects_assigned -= 0
            t.coach.save()
    t.status = 'CNL'
    t.save()
    messages.success(request, 'Ticket has been successfully cancelled')
    return HttpResponseRedirect("/tutee/home")
    
## NEEDS TO BE CORRECTED??    
@login_required
def cancel_ticket_INCORRECT(request, pid="no"):
    if pid.isdigit()==False:
        return render_to_response('/tutee/home')
    t = Ticket.objects.get(id=int(pid))
    if t.status == 'CSB':
        request.user.tuteeuser.open_project = False
        request.user.tuteeuser.save()
        t.status = 'TCF'
        t.save()
    else:
        messages.error(request, 'NOTE: Unexpected error!')
        return HttpResponseRedirect("/tutee/home")
    messages.success(request, 'Meeting details for ticket has been confirmed')
    return HttpResponseRedirect("/tutee/home")
    
    

@login_required    
def project_coach(request, pid = "nope"):
    if not request.user.groups.filter(name="coach").exists():
        return HttpResponseRedirect('/no_access/')
    if pid.isdigit() == False:
        return HttpResponseRedirect('/no_access/')
    form = TicketNoteForm()
    to_submit = []
    details = []
    withdraw = []
    p = Ticket.objects.get(id = int(pid))
    tix_details = None
    try:
        tix_details = TicketDetails.objects.get(ticket=p)
    except:
        None
    vid = None
    try:
        vid = TicketVideoURL.objects.get(ticket=p)
    except:
        try:
            vid = TicketVideo.objects.get(ticket=p)
        except: 
            messages.error(request, 'Unexpected Error: Cannot identify video submission. Please report this to the CSCC team using the REPORT page.')
    # ensures that this ticket is actually assigned to the coach requesting details
    if p.coach.user != request.user:
        return HttpResponseRedirect('/no_access/')
    if p.status ==  'CAS':    #for now, assume only 3
        stat = "waiting to conduct meeting and submit details"
        withdraw.append(1)
        to_submit.append(1)
    elif p.status == 'CSB' or p.status=='TCF':
        stat = "meeting details completed, waiting for tutee confirmation of meeting"
        details.append(1)
    elif p.status == 'APR':
        stat ="meeting complete, request closed"
        details.append(1)
    elif p.status == 'NAP':
        stat ="[Not Approved by Admin] meeting complete, request closed"
        details.append(1)
    elif p.status== 'CNL':
        stat="request cancelled"
    else:
        stat="UNKNOWN--contact administrator"
    return render_to_response('coach_project.html', {'form': form, 'p':p, 'stat': stat, 'withdraw':withdraw, 'to_submit':to_submit, 'details':details, 'tix_details':tix_details, 'vid':vid}, context_instance = RequestContext(request))
  
def coach_withdraw_ticket(request, pid="nope"):
    if not request.user.groups.filter(name="coach").exists():
        return HttpResponseRedirect('/no_access/')
    if pid.isdigit() == False:
        return HttpResponseRedirect('/no_access/')
    if request.method=="POST":
        form = TicketNoteForm(request.POST)
        if form.is_valid():
            note = TicketNote()
            tix = Ticket.objects.get(id=pid)
            note.ticket = tix
            note.coach=request.user.coachuser
            note.details=request.POST['details']
            note.save()
            tix.status = 'NAS'
            tix.save()
            tix.coach.projects_assigned -= 1
            tix.coach.save()
            tix.coach=None
            tix.save()
            messages.success(request, 'You have successfully submitted a withdrawal for your ticket assignment.')
            # email notification to ADMIN users
            admin_emails = get_admin_emails()
            email = EmailMessage('[CSCC Action Required] Ticket Needs Coaching Assignment', 'A Ticket needs a new Coaching assignment.\n \nCSCC Auto-Notifications', to=admin_emails)
            email.send()
            return HttpResponseRedirect('/coach/home/')
        else:
            messages.error(request, 'You must write a statement explaining your reason for withdrawing from this assignment.')
    return HttpResponseRedirect('/coach/ticket_'+pid)    

   
@login_required
def tutee_profile(request):
    if not request.user.groups.filter(name="tutee").exists():
        return HttpResponseRedirect('/no_access/')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            #ensure new passwords are identical
            #NOTE: does NOT currently check if old password is a match
            if request.POST['new1'] == request.POST['new2']:
                request.user.set_password(str(request.POST['new1']))
                request.user.save()
                messages.success(request, "Your password has been successfully changed.")
            else:
                messages.error(request, "Your new passwords do not match.")
    form = ChangePasswordForm()
    return render_to_response('tutee_profile.html', {'form':form, 'request':request,}, context_instance=RequestContext(request))
    
@login_required
def coach_profile(request):
    if not request.user.groups.filter(name="coach").exists():
        return HttpResponseRedirect('/no_access/')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            #ensure new passwords are identical
            #NOTE: does NOT currently check if old password is a match
            if request.POST['new1'] == request.POST['new2']:
                request.user.set_password(str(request.POST['new1']))
                request.user.save()
                messages.success(request, "Your password has been successfully changed.")
            else:
                messages.error(request, "Your new passwords do not match.")
    form = ChangePasswordForm()
    return render_to_response('coach_profile.html', {'form':form, 'request':request,}, context_instance=RequestContext(request))

    
@login_required
def submit_mtg_details(request, pid = "nope"):
    if not request.user.groups.filter(name="coach").exists():
        return HttpResponseRedirect('/no_access/')
    if pid.isdigit() == False:
        return HttpResponseRedirect('/no_access/') 
    p=Ticket.objects.get(id=pid)
    if request.method == 'POST':
        formA = TicketDetailsForm(request.POST)
        formB = TicketVideoForm(request.POST, request.FILES)
        if formA.is_valid():
            if formB.is_valid():
                if len(str(request.POST['vid_url']))==0:
                    if len(str(request.FILES['vid_file']))==0:
                        messages.error(request, "ERROR: You must chose ONE of the video options to complete the submission process")
                        return HttpResponseRedirect('/coach/submit_meeting_details/ticket_'+pid)
                    else: 
                        vid_file = TicketVideo()
                        vid_file.ticket = p
                        vid_file.video = request.FILES['vid_file']
                        vid_file.save()
                        det = TicketDetails()
                        det.ticket = p
                        det.meeting_details = request.POST['meeting_details']
                        det.meeting_duration = request.POST['meeting_duration']
                        det.meeting_date = request.POST['meeting_date']
                        det.save()
                        p.status='CSB'
                        p.save()
                        messages.success(request, 'Meeting Details have been successfully submitted for ticket "'+p.title+'"')
                        # email notification to ADMIN users
                        admin_emails = get_admin_emails()
                        email = EmailMessage('[CSCC Action Required] Ticket Review', 'A Ticket has been submitted with meeting details; review and approval needed.\n \nCSCC Auto-Notifications', to=admin_emails)
                        email.send()
                        return HttpResponseRedirect('/coach/home/')
                else:
                    vid_url = TicketVideoURL()
                    vid_url.ticket = p
                    vid_url.video_url = request.POST['vid_url']
                    vid_url.save()
                    det = TicketDetails()
                    det.ticket = p
                    det.meeting_details = request.POST['meeting_details']
                    det.meeting_duration = request.POST['meeting_duration']
                    det.meeting_date = request.POST['meeting_date']
                    det.save()
                    p.status='CSB'
                    p.save()
                    messages.success(request, 'Meeting Details have been successfully submitted for ticket "'+p.title+'"')
                    return HttpResponseRedirect('/coach/home/')
                    print "found a url"
            messages.error(request, "ERROR: please supply a valid URL for your video submission")
        return HttpResponseRedirect("/coach/submit_meeting_details/ticket_"+pid)
    else:
        formA = TicketDetailsForm(initial = {'meeting_date':datetime.date.today})
        formB = TicketVideoForm()
    return render_to_response('submit_mtg_details.html', {'formA':formA, 'formB':formB, 'p':p}, context_instance=RequestContext(request))
    
def handle_uploaded_file(file):
    if file:
        destination = open('/tmp/'+file.name, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

@login_required        
def report_coach(request):
    if not request.user.groups.filter(name="coach").exists():
        return HttpResponseRedirect('/no_access/')
    admin_email = get_admin_emails()
    if request.method == 'POST':
        form = EmailAdminForm(request.POST)
        if form.is_valid():
            email = EmailMessage('[CSCC PROBLEM REPORT] '+request.POST['subject'], 'SENT FROM COACH USERNAME: '+str(request.user.username)+', EMAIL: '+ str(request.user.email)+'\n\n'+request.POST['message'], to=admin_email)
            email.send()
            messages.success(request, 'Report notification sent to ADMIN')
            return HttpResponseRedirect("/coach/home")
    else:
        form = EmailAdminForm()
    return render_to_response('report_coach.html', {'form':form}, context_instance=RequestContext(request))

@login_required        
def report_tutee(request):
    if not request.user.groups.filter(name="tutee").exists():
        return HttpResponseRedirect('/no_access/')
    admin_email = get_admin_emails()
    if request.method == 'POST':
        form = EmailAdmin(request.POST)
        if form.is_valid():
            email = EmailMessage('[CSCC PROBLEM REPORT] '+request.POST['subject'], 'SENT FROM TUTEE USERNAME: '+str(request.user.username)+', EMAIL: '+ str(request.user.email)+'\n\n'+request.POST['message'], to=admin_email)
            email.send()
            messages.success(request, 'Report notification sent to ADMIN')
            return HttpResponseRedirect("/tutee/home")
    else:
        form = EmailAdminForm()
    return render_to_response('report_tutee.html', {'form':form}, context_instance=RequestContext(request))

@login_required 
def admin_view_requests(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/no_access/')
    for each in Ticket.objects.all():
        print each.status
    to_assign = list(Ticket.objects.filter(status='NAS'))
    assigned = list(Ticket.objects.filter(status='CAS'))
    submitted = list(Ticket.objects.filter(status='CSB'))
    approval = list(Ticket.objects.filter(status='TCF'))
    return render_to_response('all_projects_admin.html', { 'to_assign': to_assign, 'assigned': assigned, 'submitted': submitted, 'approval': approval}, context_instance = RequestContext(request))

## NEED TO CORRECT THIS
@login_required
def confirm_ticket(request, pid="none"):
    if not request.user.groups.filter(name="tutee").exists():
        return HttpResponseRedirect('/no_access/')
    if pid.isdigit() == False:
        return HttpResponseRedirect('/no_access')
    tix = Ticket.objects.get(id=int(pid))
    tix.status = 'TCF'
    tix.save()
    tix.coach.projects_assigned -= 1
    tix.coach.save()
    tuteeuser = TuteeUser.objects.get(user = request.user)
    tuteeuser.open_project = False
    tuteeuser.save()
    messages.success(request, "You have accepted the meeting details of this ticket as submitted by your Coach.")
    return HttpResponseRedirect('/tutee/ticket_'+pid)

@login_required
def reject_ticket(request, pid="none"):
    if not request.user.groups.filter(name="tutee").exists():
        return HttpResponseRedirect('/no_access/')
    if pid.isdigit() == False:
        return HttpResponseRedirect('/no_access')
    tix = Ticket.objects.get(id=int(pid))
    tix.status='CAS'
    tix.save()
    detail = TicketDetails.objects.get(ticket=tix)
    detail.delete()
    try: 
        vid = TicketVideo.objects.get(ticket=tix)
        vid.delete()
    except:
        try:
            vid = TicketVideoURL.objects.get(ticket=tix)
            vid.delete()
        except:
            None
    messages.success(request, "You have rejected the meeting details of this ticket.  Your Coach must re-submit the meeting details.")
    return HttpResponseRedirect('/tutee/ticket_'+pid)

@login_required    
def admin_coach_requests(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/no_access/')
    req = list(CoachRequest.objects.filter(status='OP'))
    return render_to_response('view_coach_requests.html', {'req':req}, context_instance = RequestContext(request))

def assignment_email(tutee, coach):
    for_tutee = "Hi "+ str(tutee.user.first_name)+"! \n \nThank you for being a part of the Course 6 Communication Center (CSCC).  You have been assigned to a coach for your recent request.  It is your responsibility to contact your coach directly and arrange the details of a meeting. \n \nYour coach is "+str(coach.user.first_name)+" "+str(coach.user.last_name)+" and can they can be reached via "+str(coach.user.email)+". \n  \nThank you, from the CSCC Team! \n \nNote: Please do not respond to this email as it is not monitored."
    for_coach = "Hi "+ str(coach.user.first_name)+"! \n  \nThank you for being a part of the Course 6 Communication Center (CSCC).  You have been assigned to a new request.  It is your responsibility to contact your tutee directly and arrange the details of a meeting. \n \nYour tutee is "+str(tutee.user.first_name)+" "+str(tutee.user.last_name)+" and can they can be reached via "+str(tutee.user.email)+". \n  \nThank you, from the CSCC Team! \n \nNote: Please do not respond to this email as it is not monitored."
    return [for_tutee, for_coach]

@login_required
def assign_coach(request, pid="nope"):
    if not request.user.groups.is_superuser:
        return HttpResponseRedirect('/no_access/')
    if pid.isdigit() == False:
        return HttpResponseRedirect('/no_access/')
    p = Project.objects.get(id=int(pid))
    if p.status != 'NAS':
        return HttpResponseRedirect('/no_access/')
    if request.method == 'POST':
        cid = int(request.POST['coach'])
        c = User.objects.get(id=cid).coachuser
        p.coach = c
        p.status =3
        p.save()
        message = assignment_email(p.tutee, p.coach)
        email_tutee = EmailMessage('[CSCC] You have a Coach!', message[0], to=[str(p.tutee.user.email), 'eunicegiarta@gmail.com'])
        email_coach = EmailMessage('[CSCC] You have a New Assignment!', message[1], to=[str(p.coach.user.email), 'eunicegiarta@gmail.com'])
        email_tutee.send()
        email_coach.send()
        
        messages.success(request, 'Coach Assignment has beeen made and the TUTEE and COACH have been notified via email')
        return HttpResponseRedirect("/app_admin/home")
    coaches = list(CoachUser.objects.all())
    return render_to_response('assign_coach.html', {'p':p, 'coaches':coaches}, context_instance = RequestContext(request))
    
@login_required
def admin_view_request(request, pid="nope"):
    if request.user.is_superuser !=True:
        return HttpResponseRedirect('/no_access/')
    if pid.isdigit()==False:
        return HttpResponseRedirect('/no_access')
    p = Ticket.objects.get(id=int(pid))
    tix_details = None
    try:
        tix_details = TicketDetails.objects.get(ticket=p)
    except:
        None
    vid = None
    try:
        vid = TicketVideoURL.objects.get(ticket=p)
    except:
        try:
            vid = TicketVideo.objects.get(ticket=p)
        except:
            None
    assign = False
    approve = False
    if p.status == 'NAS':
        assign=True
    if p.status =='TCF':
        approve=True
    return render_to_response('admin_project.html', {'p':p, 'approve':approve, 'assign':assign, 'vid':vid, 'tix_details':tix_details}, context_instance = RequestContext(request))
        
@login_required
def admin_all_tutee(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/no_access/')
    tutees = TuteeUser.objects.all()
    return render_to_response('admin_all_tutee.html', {'tutees': tutees}, context_instance = RequestContext(request))
    
@login_required
def admin_all_coach(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/no_access/')
    coaches = CoachUser.objects.all()
    return render_to_response('admin_all_coach.html', {'coaches': coaches}, context_instance = RequestContext(request))

@login_required
def add_coach(request, pid):
    r = CoachRequest.objects.get(id=int(pid))
    if not request.user.is_superuser:
        return HttpResponseRedirect('/no_access/')
    if pid.isdigit() == False:
        return HttpResponseRedirect('/no_access/')
    password = User.objects.make_random_password()
    new = User.objects.create_user(username=r.athena, email=r.athena+'@mit.edu', password=password)
    new.first_name = r.first_name
    new.last_name = r.last_name
    new.groups.add(Group.objects.get(name='coach'))
    new.save()
    c = CoachUser()
    c.user = new
    c.phone = r.phone
    c.course = r.course
    c.projects_assigned = 0
    c.save()
    r.status = 'AC'
    r.save()
    email_coach = EmailMessage('[CSCC] Congratulations, you are now a COACH for CSCC!', "Welcome to the CSCC community, "+new.first_name+"!\nWe will contact you when an assignment has been made.  You can also check your assignments by logging in. \n\nusername: "+new.username+" \n\npassword: "+password+"\n\nThanks,\nThe CSCC Team\n\n\nDo not respond to this email as it is unmoderated.  Use the REPORT page to contact us.", to=[new.email])
    email_coach.send()
    messages.success(request, str(new.username)+" has been assigned as coach and notified by email.")
    return HttpResponseRedirect('/app_admin/coach_requests/')

@login_required    
def reject_coach_req(request, pid="none"):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/no_access/')
    if pid.isdigit() ==False:
        message.error(request, "ERROR: Incorrect UID for CoachRequest instance")
        return HttpResponseRedirect('/app_admin/home/')
    r = CoachRequest.objects.get(id=int(pid))
    r.status = 'RJ'
    r.save()
    return HttpResponseRedirect('/app_admin/coach_requests/')

@login_required
def admin_profile(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/no_access/')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            #ensure new passwords are identical
            #NOTE: does NOT currently check if old password is a match
            if request.POST['new1'] == request.POST['new2']:
                request.user.set_password(str(request.POST['new1']))
                request.user.save()
                messages.success(request, "Your password has been successfully changed.")
            else:
                messages.error(request, "Your new passwords do not match.")
    form = ChangePasswordForm()
    return render_to_response('admin_profile.html', {'form':form, 'request':request,}, context_instance=RequestContext(request))

@login_required
def admin_approve_ticket(request, pid="none"):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/no_access/')
    if pid.isdigit() ==False:
        return HttpResponseRedirect('/no_access/')
    tix = Ticket.objects.get(id=int(pid))
    tix.status='APR'
    tix.save()
    messages.success(request, "You have APPROVED this ticket.")
    return HttpResponseRedirect('/app_admin/ticket_'+pid)

@login_required
def admin_reject_ticket(request, pid="none"):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/no_access/')
    if pid.isdigit() ==False:
        return HttpResponseRedirect('/no_access/')
    tix = Ticket.objects.get(id=int(pid))
    tix.status='NAP'
    tix.save()
    messages.success(request, "You have REJECTED this ticket.")
    return HttpResponseRedirect('/app_admin/ticket_'+pid)

@login_required
def admin_view_coach(request, pid="none"):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/no_access/')
    if pid.isdigit() ==False:
        message.error(request, "ERROR: Incorrect UID for Coach instance")
        return HttpResponseRedirect('/app_admin/home/')
    c = CoachUser.objects.get(id=int(pid))
    prev_tix = list(c.ticket_set.all())
    open_tix = []
    pending = []
    
    for each in prev_tix:
        if each.status == 'CAS':
            open_tix.append(each)
            prev_tix.remove(each)
        elif each.status == 'CSB':
            pending.append(each)
            prev_tix.remove(each)
        # this leaves 'APR', 'NAP', and 'TCF' and possibly 'CNL' 
    return render_to_response('admin_view_coach.html', {'c':c, 'past':prev_tix, 'open':open_tix, 'pending': pending}, context_instance=RequestContext(request)) 
    
@login_required
def view_coach_hours(request, pid="none"):
    if not request.user.is_superuser:
        return HttpdResponseRedirect('/no_access/')
    if pid.isdigit() == False:
        return HttpResponseRedirect('/no_access/')
    c = CoachUser.objects.get(id=int(pid))
    tix = list(c.ticket_set.filter(status='APR')) + list(c.ticket_set.filter(status='NAP')) + list(c.ticket_set.filter(status='TCF'))
    dets = []
    hrs_approve = 0
    hrs_pending = 0
    hrs_reject = 0
    for each in tix:
        dets.append(each.ticketdetails)
        if each.status =='APR':
            hrs_approve += each.ticketdetails.meeting_duration/60.0
        elif each.status =='TCF':
            hrs_pending += each.ticketdetails.meeting_duration/60.0
        elif each.status =='NAP':
            hrs_reject += each.ticketdetails.meeting_duration/60.0
    dets.sort(key=lambda r: r.meeting_date)
    
    return render_to_response('admin_view_coach_hours.html', {'request':request, 'c':c, 'dets':dets, 'hrs_approve': hrs_approve, 'hrs_pending':hrs_pending, 'hrs_reject': hrs_reject}, context_instance=RequestContext(request))
    
   
@login_required  
def assign_ticket(request, pid="none"):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/no_access/')
    if pid.isdigit() ==False:
        message.error(request, "ERROR: Incorrect UID for Coach instance")
        return HttpResponseRedirect('/app_admin/home/')
    coaches = CoachUser.objects.all().order_by('projects_assigned')
    if request.method == 'POST':
           cid = int(request.POST['coach'])
           c = CoachUser.objects.get(id=cid)
           c.projects_assigned += 1
           c.save()
           p = Ticket.objects.get(id=int(pid))
           p.coach = c
           p.status ='CAS'
           p.save()
           message = assignment_email(p.tutee, p.coach)
           email_tutee = EmailMessage('[CSCC] You have a Coach!', message[0], to=[str(p.tutee.user.email)])
           email_coach = EmailMessage('[CSCC] You have a New Assignment!', message[1], to=[str(p.coach.user.email)])
           email_tutee.send()
           email_coach.send()

           messages.success(request, 'Coach Assignment has beeen made and the TUTEE and COACH have been notified via email')
           return HttpResponseRedirect("/app_admin/home")
    
    return render_to_response('assign_coach.html', {'p':Ticket.objects.get(id=int(pid)), 'coaches':coaches}, context_instance = RequestContext(request))
   
@login_required
def add_new_admin(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/no_access/')
    if request.method=="POST":
        form = NewAdminForm(request.POST)
        if form.is_valid():
            password = User.objects.make_random_password()
            new = User.objects.create_superuser(username=request.POST['username'], email=request.POST['username']+'@mit.edu', password=password)
            new.first_name = request.POST['first_name']
            new.last_name = request.POST['last_name']
            new.save()
            email_new_admin = EmailMessage('[CSCC] Congratulations, you are now an ADMIN for CSCC!', "Welcome to the CSCC community, "+new.first_name+"!\nYou can access your account with the following login information:\n\nusername: "+new.username+" \n\npassword: "+password+"\n\nThanks for joining us,\nThe CSCC Team (+ you)\n\n\nDo not respond to this email as it is unmoderated.", to=[new.email])
            email_new_admin.send()
            messages.success(request, "A new ADMIN account has been created and an email has been sent notifying "+new.first_name+" about their new position.")
            HttpResponseRedirect("/app_admin/home/")
    else:
        form = NewAdminForm()
    return render_to_response('admin_add_new.html', {'form':form}, context_instance=RequestContext(request))
