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

def basecase_home(request):
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
            n.email = request.POST['email']
            n.phone = request.POST['phone']
            n.uat_semester = request.POST['uat_semester']
            n.uat_year =request.POST['uat_year']
            n.course =request.POST['course']
            n.save()
            messages.success(request, 'Application successfully submitted.  Thank you for your interest in becoming a coach with CSCC.  We will be in contact with you shortly!')
            return HttpResponseRedirect('/uap_app/')
        else:
            messages.error(request, 'NOTE: Your coach application was not submitted properly.  Please try again!')
            return HttpResponseRedirect('/uap_app/coach/request/')
                
        return render_to_response('coach_application.html', {'form': form, 'user': request.user }, context_instance=RequestContext(request)) #CHANGE THIS 
    form = CoachReqForm()
    return render_to_response('coach_application.html', {'form': form}, context_instance=RequestContext(request))
    
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
            tu.email = str(d['email'])
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
    

def logging_in(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_staff:
                    return HttpResponseRedirect('/uap_app/admin/home')
                try: 
                    CoachUser.objects.get(user__id=request.user.id)
                    print 'logged in COACH'
                    return HttpResponseRedirect('/uap_app/coach/home/')
                except:
                    try: 
                        TuteeUser.objects.get(user__id=request.user.id)
                        print 'logged in TUTEE'
                        return HttpResponseRedirect('/uap_app/tutee/home/')
                    except: 
                        try:
                            AdminUser.objects.get(user__id =request.user.id)
                            print 'logged in ADMIN'
                            return HttpResponseRedirect('/uap_app/admin/home/')
                        except:
                            print 'PROBLEM--DID NOT FIND TYPE USER BUT EXISTS'
                            return HttpResponseRedirect('uap_app/home/success')
            else:
                print 'not logged in, not active'
                return HttpResponseRedirect('uap_app/home/failure')            
        else:
                messages.error(request, 'Login information is incorrect')
                return render_to_response('login.html', context_instance=RequestContext(request))
    return render_to_response('login.html', context_instance=RequestContext(request))

def logging_out(request):
    logout(request)
    return render_to_response('logout.html', context_instance=RequestContext(request))
    
"""
A TuteeUser opens a new project; new project is created IF no open projects
"""
def new_project_added(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/uap_app/login')
    if request.method =='POST':
        if form.is_valid():
            if curruser.open_project == False:  #CURRENT USER
                proj = Project()
                proj.title = form.data['title']
                proj.description = form.data['description']
                proj.status = 1
                proj.tutee = curruser #CURRENT USER
                proj.expiry_data = form.data['expiry_date']
                proj.save()
                
                curruser.open_project = True
    return render_to_response('uap_app/new_project_added.html', {'user': user, 'summary': summary, 'ordered_people': ordered_people, 'getting':l_get, 'paying': l_owe})
    
@login_required
def new_project(request):
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
                try: 
                    form.data['ee_request']         #check if TUTEE indicated EE-related
                    t.ee_related = True
                except:
                    t.ee_related = False
                try:
                    form.data['cs_request']         #check if TUTEE indicated CS-related
                    t.cs_related = True
                except:
                    t.cs_related = False
                t.area_of_interest = form.data['area_of_interest']
                t.save()
                curruser.open_project = True
                curruser.save()
                messages.success(request, 'You have successfully created a new Project')
                return render_to_response('homebase.html', context_instance=RequestContext(request))
            else:
                messages.error(request, 'NOTE: An unexpected error has occurred, ticket not created.')
                return render_to_response('homebase.html', context_instance=RequestContext(request))
                
        return render_to_response('new_project.html', {'form': form, 'user': request.user }, context_instance=RequestContext(request)) #CHANGE THIS 
    
    form = TicketForm()
    return render_to_response('new_project.html', {'form': form}, context_instance=RequestContext(request))
    
def home_success(request):
    messages.success(request, 'You have successfully created a new Project')
    print "********"+ request.user.username + " is logged in"
    return render_to_response('homebase.html', context_instance=RequestContext(request))
    
def home_success_tutee(request):
    messages.success(request, 'You have successfully created a new Project')
    print "********"+ request.user.username + " is logged in"
    return render_to_response('homebase.html', {'request':request}, context_instance=RequestContext(request))

@login_required    
def home_tutee(request):
    print "********"+ request.user.username + " is logged in"
    new = [1]
    tickets = []
    current = None
    if request.user.tuteeuser.open_project:
        new.remove(1)
        tickets = list(request.user.tuteeuser.ticket_set.all())
        for each in tickets:
            if each.status == 'NAS' or each.status=='CAS' or each.status=='CSB':
                current = each
    return render_to_response('homebase.html', {'request':request, 'current': current, 'new': new}, context_instance=RequestContext(request))
    
@login_required    
def home_coach(request):
    print "********"+ request.user.username + " is logged in"
    return render_to_response('home_coach.html', {'request':request}, context_instance=RequestContext(request))
    
@login_required    
def home_admin(request):
    print "********"+ request.user.username + " is logged in"
    return render_to_response('home_admin.html', {'request':request}, context_instance=RequestContext(request))

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
def project_details_admin(request):
    p = Project.objects.get(id=1)
    return render_to_response('project_details.html', {'p': p}, context_instance=RequestContext(request))


@login_required
def all_requests_tutee(request):
    u = request.user
    t = u.tuteeuser
    past_tix = list(t.ticket_set.all())
    curr = []
    create = [1]

    if t.open_project:
        create.remove(1)
        for each in past_tix:
            if each.status != 'TCF' and each.status != 'APR' and each.status != 'CNL':
                curr.append(each)
                past_tix.remove(each)
                break

    return render_to_response('all_projects_tutee.html', {'u': u, 't':t, 'projects':past_tix, 'curr':curr, 'create': create}, context_instance=RequestContext(request)) 
    
        
@login_required
def all_requests_coach(request):
    u = request.user
    c = u.coachuser
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
        # this leaves 'APR' and 'TAP' and possibly 'CNL' 
    return render_to_response('all_projects_coach.html', {'u': u, 'c':c, 'past':prev_tix, 'open':open_tix, 'pending': pending}, context_instance=RequestContext(request)) 

@login_required    
def project_tutee(request, pid = "nope"):
    if request.user.groups.filter(name='tutee').exists() != True:
        return HttpResponseRedirect('uap_app/home/')
    if pid.isdigit() == False:
        return render_to_response('uap_app/home/failure', context_instance = RequestContext(request))
    confirm = []
    details = []
    p = Ticket.objects.get(id = int(pid))
    if p.status == 'NAS':
        stat = "waiting for coach assignment"
    elif p.status == 'CAS':
        stat = "coach assigned, waiting for meeting details"
    elif p.status == 'CSB':
        stat = "meeting details completed, waiting for your confirmation of meeting"
        details.append(1)
        confirm.append(1)
    elif p.status =='TCF' or p.status =='APR':
        stat ="meeting complete, request closed"
        details.append(1)
    elif p.status=='CNL':
        stat="request was cancelled"
    else:
        stat="UNKNOWN--contact administrator"
    return render_to_response('tutee_project.html', {'p':p, 'stat': stat, 'confirm':confirm, 'details':details}, context_instance = RequestContext(request))
   
@login_required
def cancel_ticket(request, pid="no"):
    if pid.isdigit()==False:
        return render_to_response('/uap_app/tutee/home')
    t = Ticket.objects.get(id=int(pid))
    if t.status == 'NAS' or t.status == 'CAS':
        request.user.tuteeuser.open_project = False
        request.user.tuteeuser.save()
    t.status = 'CNL'
    t.save()
    messages.success(request, 'Ticket has been successfully cancelled')
    return HttpResponseRedirect("/uap_app/tutee/home")
    
@login_required
def cancel_ticket(request, pid="no"):
    if pid.isdigit()==False:
        return render_to_response('/uap_app/tutee/home')
    t = Ticket.objects.get(id=int(pid))
    if t.status == 'CSB':
        request.user.tuteeuser.open_project = False
        request.user.tuteeuser.save()
        t.status = 'TAP'
        t.save()
    else:
        messages.error(request, 'NOTE: Unexpected error!')
        return HttpResponseRedirect("/uap_app/tutee/home")
    messages.success(request, 'Meeting details for ticket has been confirmed')
    return HttpResponseRedirect("/uap_app/tutee/home")
    
    

@login_required    
def project_coach(request, pid = "nope"):
    if pid.isdigit() == False:
        return render_to_response('/uap_app/home/failure', context_instance = RequestContext(request))
    if request.method =='POST':
        form = WithdrawNoteForm(request.POST)
        if form.is_valid():
            note = ReassignNote(coach = request.user.coachuser, project = Project.objects.get(id=int(pid)), details = request.POST['details'])
            p = Ticket.objects.get(id=int(pid))
            p.status = 7
            p.save()
            messages.success(request, 'Your Profile has been successfully updated')
            return HttpResponseRedirect("/uap_app/coach/home")
    else:
        form = WithdrawNoteForm()
    to_submit = []
    details = []
    withdraw = []
    p = Project.objects.get(id = int(pid))
    if p.status ==  2 or p.status == 3:    #for now, assume only 3
        stat = "waiting to conduct meeting and submit details"
        withdraw.append(1)
        to_submit.append(1)
    elif p.status ==4:
        stat = "meeting details completed, waiting for tutee confirmation of meeting"
        details.append(1)
    elif p.status == 5 or p.status ==6:
        stat ="meeting complete, request closed"
        details.append(1)
    elif p.status==8:
        stat="request cancelled"
    else:
        stat="UNKNOWN--contact administrator"
    return render_to_response('coach_project.html', {'form': form, 'p':p, 'stat': stat, 'withdraw':withdraw, 'to_submit':to_submit, 'details':details}, context_instance = RequestContext(request))
   
@login_required
def tutee_profile(request):
    u = request.user
    t = u.tuteeuser
    if request.method =='POST':
        form = TuteeUserProfileForm(request.POST)
        if form.is_valid():
            u.email = request.POST['email']
            u.save()
            if request.POST.has_key('ee_request')==False:
                t.ee_request = False
            else:
                t.ee_request = request.POST['ee_request']
            if request.POST.has_key('cs_request')==False:
                t.cs_request = False
            else:
                t.cs_request = request.POST['cs_request']
            t.area_of_interest = request.POST['area_of_interest']
            t.research_advisor = request.POST['research_advisor']
            t.research_advisor_email = request.POST['research_advisor_email']
            t.phone = request.POST['phone']
            t.save()
            messages.success(request, 'Your Profile has been successfully updated')
            return render_to_response('tutee_profile.html', {'t':t, 'request':request, 'u':u}, context_instance=RequestContext(request))
    else:
        initial=dict(email = u.email, phone = t.phone, research_advisor = t.research_advisor, research_advisor_email = t.research_advisor_email, ee_request = t.ee_request, cs_request = t.cs_request, area_of_interest = t.area_of_interest)
        form = TuteeUserProfileForm(initial)
    return render_to_response('tutee_profile.html', {'form':form, 't':t, 'request':request, 'u':u}, context_instance=RequestContext(request))
    
@login_required
def coach_profile(request):
    u = request.user
    t = u.coachuser
    if request.method =='POST':
        form = CoachUserProfileForm(request.POST)
        if form.is_valid():
            u.email = request.POST['email']
            u.save()
            if request.POST.has_key('ee_help')==False:
                t.ee_help = False
            else:
                t.ee_help = request.POST['ee_help']
            if request.POST.has_key('cs_help')==False:
                t.cs_help = False
            else:
                t.cs_help = request.POST['cs_help']
            t.phone = request.POST['phone']
            t.save()
            messages.success(request, 'Your Profile has been successfully updated')
            return render_to_response('coach_profile.html', {'t':t, 'request':request, 'u':u}, context_instance=RequestContext(request))
    else:
        initial=dict(email = u.email, phone = t.phone, ee_help = t.ee_help, cs_help = t.cs_help)
        form = CoachUserProfileForm(initial)
    return render_to_response('coach_profile.html', {'form':form, 't':t, 'request':request, 'u':u}, context_instance=RequestContext(request))

    
@login_required
def submit_mtg_details(request, pid = "nope"):
    if pid.isdigit() == False:
        return render_to_response('uap_app/home/failure', context_instance = RequestContext(request)) ##CHANGE THIS  
    p=Project.objects.get(id=pid)
    if request.method == 'POST':
        form = SubmitProjectForm(request.POST, request.FILES)
        if form.is_valid():
            print request.FILES['video']
            p.video = request.FILES['video']
            p.meeting_details = request.POST['meeting_details']
            p.meeting_duration = request.POST['meeting_duration']
            p.meeting_date = request.POST['meeting_date']
            p.status = 4
            p.save()
            print p.meeting_details
            messages.success(request, 'Meeting Details for Request #'+str(pid)+' has been successfully submitted')
            return HttpResponseRedirect("/uap_app/coach/home")
    else:
        form = SubmitProjectForm(initial = {'meeting_date':datetime.date.today})
    return render_to_response('submit_mtg_details.html', {'form':form, 'pid':pid}, context_instance=RequestContext(request))
    
def handle_uploaded_file(file):
    if file:
        destination = open('/tmp/'+file.name, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

@login_required        
def report_coach(request):
    admin_email = ['eunicegiarta@gmail.com']
    if request.method == 'POST':
        form = EmailAdminForm(request.POST)
        if form.is_valid():
            admin = list(User.objects.filter(is_staff=True))
            for each in admin:
                admin_email.append(each.email)
            email = EmailMessage('[CSCC PROBLEM REPORT] '+request.POST['subject'], 'SENT FROM COACH USERNAME: '+str(request.user.username)+', EMAIL: '+ str(request.user.email)+'\n\n'+request.POST['message'], to=admin_email)
            email.send()
            messages.success(request, 'Report notification sent to ADMIN')
            return HttpResponseRedirect("/uap_app/coach/home")
    else:
        form = EmailAdminForm()
    return render_to_response('report_coach.html', {'form':form}, context_instance=RequestContext(request))

@login_required        
def report_tutee(request):
    admin_email = ['eunicegiarta@gmail.com']  #add myself for debugging purposes
    if request.method == 'POST':
        form = EmailAdmin(request.POST)
        if form.is_valid():
            admin = list(User.objects.filter(is_staff=True))
            for each in admin:
                admin_email.append(each.email)
                email = EmailMessage('[CSCC PROBLEM REPORT] '+request.POST['subject'], 'SENT FROM TUTEE USERNAME: '+str(request.user.username)+', EMAIL: '+ str(request.user.email)+'\n\n'+request.POST['message'], to=admin_email)
                email.send()
            messages.success(request, 'Report notification sent to ADMIN')
            return HttpResponseRedirect("/uap_app/tutee/home")
    else:
        form = EmailAdminForm()
    return render_to_response('report_tutee.html', {'form':form}, context_instance=RequestContext(request))

@login_required 
def admin_view_requests(request):
    to_assign = list(Ticket.objects.filter(status='NAS'))
    assigned = list(Ticket.objects.filter(status='TAS'))
    submitted = list(Ticket.objects.filter(status='CSB'))
    approval = list(Ticket.objects.filter(status='TAP'))
    return render_to_response('all_projects_admin.html', { 'to_assign': to_assign, 'assigned': assigned, 'submitted': submitted, 'approval': approval}, context_instance = RequestContext(request))
def confirm_ticket(request, pid="none"):
    return 
    
def admin_coach_requests(request):
    req = list(CoachRequest.objects.filter(status='OP'))
    return render_to_response('view_coach_requests.html', {'req':req}, context_instance = RequestContext(request))
    
def assignment_email(tutee, coach):
    for_tutee = "Hi "+ str(tutee.user.first_name)+"! \n \nThank you for being a part of the Course 6 Communication Center (CSCC).  You have been assigned to a coach for your recent request.  It is your responsibility to contact your coach directly and arrange the details of a meeting. \n \nYour coach is "+str(coach.user.first_name)+" "+str(coach.user.last_name)+" and can they can be reached via "+str(coach.user.email)+". \n  \nThank you, from the CSCC Team! \n \nNote: Please do not respond to this email as it is not monitored."
    for_coach = "Hi "+ str(coach.user.first_name)+"! \n  \nThank you for being a part of the Course 6 Communication Center (CSCC).  You have been assigned to a new request.  It is your responsibility to contact your tutee directly and arrange the details of a meeting. \n \nYour tutee is "+str(tutee.user.first_name)+" "+str(tutee.user.last_name)+" and can they can be reached via "+str(tutee.user.email)+". \n  \nThank you, from the CSCC Team! \n \nNote: Please do not respond to this email as it is not monitored."
    return [for_tutee, for_coach]

@login_required
def assign_coach(request, pid="nope"):
    if pid.isdigit() == False:
        return render_to_response('uap_app/home/failure', context_instance = RequestContext(request)) ##CHANGE THIS
    p = Project.objects.get(id=int(pid))
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
        return HttpResponseRedirect("/uap_app/admin/home")
    coaches = list(CoachUser.objects.all())
    return render_to_response('assign_coach.html', {'p':p, 'coaches':coaches}, context_instance = RequestContext(request))
    
@login_required
def admin_view_request(request, pid="nope"):
    if request.user.is_superuser !=True:
        return HttpResponseRedirect('/uap_app/logout')
    if pid.isdigit()==False:
        return render_to_response('uap_app/home/failure', context_instance = RequestContext(request)) ##CHANGE THIS
    p = Ticket.objects.get(id=int(pid))
    assign = False
    if p.status == 'NAS':
        assign=True
    return render_to_response('admin_project.html', {'p':p, 'assign':assign}, context_instance = RequestContext(request))
        
@login_required
def admin_all_tutee(request):
    if request.user.is_superuser != True:
        return HttpResponseRedirect('/uap_app/logout/')
    tutees = TuteeUser.objects.all()
    return render_to_response('admin_all_tutee.html', {'tutees': tutees}, context_instance = RequestContext(request))
    
@login_required
def admin_all_coach(request):
    if request.user.is_superuser != True:
        return HttpResponseRedirect('/uap_app/logout/')
    coaches = CoachUser.objects.all()
    return render_to_response('admin_all_coach.html', {'coaches': coaches}, context_instance = RequestContext(request))

@login_required
def add_coach(request, pid):
    r = CoachRequest.objects.get(id=int(pid))
    if request.user.is_superuser != True:
        return HttpResponseRedirect('/uap_app/logout/')
    if pid.isdigit() == False:
        return render_to_response('uap_app/home/failure', context_instance = RequestContext(request)) ##CHANGE THIS
    password = User.objects.make_random_password()
    new = User.objects.create_user(username=r.athena, email=r.athena+'@mit.edu', password=password)
    new.first_name = r.first_name
    new.last_name = r.last_name
    new.save()
    c = CoachUser()
    c.user = new
    c.phone = r.phone
    c.course = r.course
    c.projects_assigned = 0
    c.save()
    r.status = 'AC'
    r.save()
    ## generate email
    email_coach = EmailMessage('[CSCC] Congratulations, you are now a COACH for CSCC!', "To login, your username is your athena: "+new.username+".  Your password is '"+password+"'.", to=[str(new.email), 'eunicegiarta@gmail.com'])
    email_coach.send()
    return HttpResponseRedirect('/uap_app/admin/coach_requests/')
    
def reject_coach_req(request, pid="none"):
    if request.user.is_superuser != True:
        return HttpResponseRedirect('/uap_app/logout/')
    if pid.isdigit() ==False:
        message.error(request, "ERROR: Incorrect UID for CoachRequest instance")
        return HttpResponseRedirect('/uap_app/admin/home/')
    r = CoachRequest.objects.get(id=int(pid))
    r.status = 'RJ'
    r.save()
    return HttpResponseRedirect('/uap_app/admin/coach_requests/')

@login_required
def admin_profile(request):
    u = request.user
    if request.method =='POST':
        form = AdminUserProfileForm(request.POST)
        if form.is_valid():
            u.email = request.POST['email']
            messages.success(request, 'Profile has been successfully updated')
            return render_to_response('home_admin.html', {'request':request}, context_instance=RequestContext(request))
    else:
        form = AdminUserProfileForm(initial = dict(email = u.email))
    return render_to_response('admin_profile.html', {'form':form, 'u':u}, context_instance = RequestContext(request))