from django.db import models
from django import forms
from django.contrib.auth.models import User, Permission
from django.forms.extras.widgets import *
from datetime import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group

  
## CHOICES 
SIX1 = '6-1'
SIX2 = '6-2'
SIX3 = '6-3'
SIX7 = '6-7'
COURSE_CHOICES = (
    (SIX1, '6-1: Electrical Engineering'),
    (SIX2, '6-2: Electrical Engineering & Computer Science'),
    (SIX3, '6-3: Computer Science and Engineering'),
    (SIX7, '6-7: Computer Science and Molecular Biology')
)   
OPEN = 'OP'
ACCEPTED = 'AC'
REJECTED = 'RJ'
COACH_APP_STATUS_CHOICES = (
    (OPEN, 'Open Request'),
    (ACCEPTED, 'Accepted'),
    (REJECTED, 'Rejected'),
)
SEMESTER_CHOICES = (
    ('SP', 'Spring'),
    ('FL', 'Fall'),
    ('NA', 'N/A')     #if not yet taken
) 
 
STATUS_CHOICES = (
    ('NAS', 'Needs Coach Assignment'),
    ('CAS', 'Coach Assigned'),
    ('CSB', 'Coach Submit Ticket'),
    ('TCF', 'Tutee Confirms Ticket'),
    ('APR', 'Admin Approval of Ticket'),
    ('NAP', 'Admin Denies Approval'),
    ('CNL', 'Cancelled Ticket')
)

class CoachRequest(models.Model):
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    athena = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    course = models.CharField(max_length=3, choices=COURSE_CHOICES)
    status = models.CharField(max_length=2, choices=COACH_APP_STATUS_CHOICES, default=OPEN)
    uat_semester = models.CharField(max_length=3, choices=SEMESTER_CHOICES)
    uat_year = models.IntegerField(max_length=4)
    
        
class CoachUser(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=11)
    course = models.CharField(max_length=3, choices=COURSE_CHOICES)
    projects_assigned = models.IntegerField(default = 0)
    
    def __string__(self):
        print self.user.username + ', Coach'
    
class TuteeUser(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=11)
    research_advisor = models.TextField()
    research_advisor_email = models.TextField()
    open_project = models.BooleanField()
    def __string__(self):
        print self.user.username + ', Tutee'
    
class AdminUser(models.Model):
    user = models.OneToOneField(User)
    
    def __string__(self):
        print self.user.username + ', Admin'


"""
Let the following integers represent the status of the Project:
** did not want to created static choices bc not sure how these will change **

1 = just initiated by TuteeUser --> AdminUser needs to assign
2 = AdminUser has assigned and awaits "acceptance" --> CoachUser needs to accept
3 = CoachUser accepts assigment
4 = CoachUser submits completion, video file uploaded
5 = TuteeUser confirms meeting
6 = AdminUser approves and "closes" the project

7 = CoachUser rejects an assignment --> AdminUser needs to reassign
8 = TuteeUser cancels the project

"""


class Ticket(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    area_of_interest = models.CharField(max_length=30)
    date_of_interest = models.DateField(null=True)   #ie. presentation date, date of defense, etc.
    date_created = models.DateField(auto_now_add=True) #date ticket created by tutee
    status = models.CharField(max_length = 3, choices = STATUS_CHOICES) 
    tutee = models.ForeignKey(TuteeUser)
    coach = models.ForeignKey(CoachUser, null=True)
    def __string__(self):
        print 'created by ' + self.tutee.user.username
    
class TicketDetails(models.Model):
    # video = models.FileField(upload_to='video/', null=True)   --- NOW WITH TicketVideo
    meeting_details = models.TextField(blank=True)      
    meeting_duration = models.IntegerField(default = 0) # length of meeting time in minutes
    meeting_date = models.DateField(null=True)      # date that the coach/tutee meeting occurred
    ticket = models.OneToOneField(Ticket)
        
class TicketVideo(models.Model):
    video = models.FileField(upload_to='video/')
    ticket = models.OneToOneField(Ticket)

class TicketVideoURL(models.Model):
    video_url = models.CharField(max_length=100)
    ticket = models.OneToOneField(Ticket)

class TicketNote(models.Model):
    ticket = models.ForeignKey(Ticket)
    details = models.TextField(blank=True)
    coach = models.ForeignKey(CoachUser)
        
class TicketForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput({ "placeholder": "Project Talk on K-lines" }), label = "Conference Talk Title")
    details = forms.CharField(widget=forms.Textarea, label="Paper Abstract (optional)")
    date_of_interest = forms.DateField(widget=forms.TextInput({ "placeholder": "YYYY-MM-DD" }), label="Approximate Conference Presentation Date")
    area_of_interest = forms.CharField(widget=forms.TextInput({ "placeholder": "ie. Artificial Intelligence" }))
    
class TicketDetailsForm(forms.Form):
    #video = forms.FileField(required = False) ##FOR NOW MUST CHANGE!!
    meeting_details = forms.CharField(widget=forms.Textarea)
    meeting_duration = forms.IntegerField(label = "Duration of Meeting (mins)", widget=forms.TextInput({ "placeholder": "ex: 1 Hour = '60'" }))
    meeting_date = forms.DateField()    

class TicketVideoForm(forms.Form):
    vid_file = forms.FileField(required = False, label="Video File")
    vid_url = forms.URLField(required = False, label="Video URL", widget=forms.TextInput({ "placeholder": "www.youtube.com/my_video1173" }))

class TicketNoteForm(forms.Form):
    details = forms.CharField(widget=forms.Textarea, label='Reason for Withdrawl')
   
class TuteeUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput({ "placeholder": "jsmith2013" }), label="Userame (Athena)")
    password = forms.CharField(widget=forms.TextInput({ "placeholder": "password123" }))
    first_name = forms.CharField(widget=forms.TextInput({ "placeholder": "Jane" }))
    last_name = forms.CharField(widget=forms.TextInput({ "placeholder": "Smith" }))
    phone = forms.CharField(max_length=11, widget=forms.TextInput({ "placeholder": "18005556789" }))
    research_advisor_email = forms.EmailField(widget=forms.TextInput({ "placeholder": "johndoe@mit.edu" }))
    
class AdminUserForm(forms.Form):
    username =  forms.CharField()
    password = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    
class AdminUserProfileForm(forms.Form):
    email = forms.EmailField()
    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

### CURRENTLY UNUSED    
class TuteeUserProfileForm(forms.Form):
    email = forms.EmailField()
    phone = forms.CharField(max_length=11)
    research_advisor_email = forms.EmailField()

### CURRENTLY UNUSED
class CoachUserProfileForm(forms.Form):
    email = forms.EmailField()
    phone = forms.CharField(max_length=11)
    ee_help = forms.BooleanField(required = False,label = "Can support EE-focus")
    cs_help = forms.BooleanField(required = False,label = "Can support CS-focus")

class EmailAdminForm(forms.Form):
    subject = forms.CharField(label="Subject")
    message = forms.CharField(widget = forms.Textarea, label="Problem Description")
    
class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
    subject = forms.CharField(label="Subject")
    message = forms.CharField(widget = forms.Textarea, label="Message")

class CoachReqForm(forms.Form):
    athena_username = forms.CharField(widget=forms.TextInput({ "placeholder": "jsmith2013" })) 
    first_name = forms.CharField(widget=forms.TextInput({ "placeholder": "Jane" }))
    last_name = forms.CharField(widget=forms.TextInput({ "placeholder": "Smith" }))  
    phone = forms.CharField(widget=forms.TextInput({ "placeholder": "15005552358" }))
    course = forms.ChoiceField(choices = COURSE_CHOICES)
    uat_semester = forms.ChoiceField(widget=forms.Select, choices = SEMESTER_CHOICES, label="Semester enrolled in 6.8UAT")
    uat_year = forms.IntegerField(label="Year enrolled in 6.UAT", widget=forms.TextInput({ "placeholder": "2012" }))

class ChangePasswordForm(forms.Form):
    current = forms.CharField(label="Current Password") 
    new1 = forms.CharField(widget=forms.PasswordInput(render_value=False), label="New Password")
    new2 = forms.CharField(widget=forms.PasswordInput(render_value=False), label="Confirm New Password")

class ValidateAgreementForm(forms.Form):
    agree = forms.BooleanField(required=True, label="I have read and agree with the terms and conditions outlined above")
    
class NewAdminForm(forms.Form)
    username = forms.CharField(label="Athena Username")
    first_name = forms.CharField()
    last_name = forms.CharField()