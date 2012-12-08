from django.db import models
from django import forms
from django.contrib.auth.models import User, Permission
from django.forms.extras.widgets import *
from datetime import *
from django.contrib.contenttypes.models import ContentType

#proj_ct = ContentType.objects.get(app_label='uap_app', model='project')
#tutee_permission = Permission(name="Tutee Permission", codename="tutee_permission", content_type = proj_ct)
#coach_permission = Permission(name="Coach Permission", codename="coach_permission", content_type = proj_ct)
#admin_permission = Permission(name="Admin Permission", codename="admin_permission", content_type = proj_ct)        
  
class CoachRequest(models.Model):
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    athena = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    ee_able = models.BooleanField()
    cs_able = models.BooleanField()

    OPEN = 'OP'
    ACCEPTED = 'AC'
    REJECTED = 'RJ'
    STATUS_CHOICES = (
        (OPEN, 'Open Request'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=OPEN)
        
class CoachUser(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=11)
    ee_help = models.BooleanField()
    cs_help = models.BooleanField()
    projects_assigned = models.IntegerField(default = 0)
    
    def __string__(self):
        print self.user.username + ', Coach'
    
class TuteeUser(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=11)
    ee_request = models.BooleanField()
    cs_request = models.BooleanField()
    area_of_interest = models.TextField()
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


class Project(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    date_of_interest = models.DateField(null=True)   #ie. presentation date, date of defense, etc.
    status = models.IntegerField() 
    tutee = models.ForeignKey(TuteeUser)
    coach = models.ForeignKey(CoachUser, null=True)
    video = models.FileField(upload_to='video/', null=True)
    meeting_details = models.TextField(blank=True)      
    meeting_duration = models.IntegerField(default = 0) # length of meeting time in minutes
    meeting_date = models.DateField(null=True)      # date that the coach/tutee meeting occurred
    
    def __string__(self):
        print 'created by ' + self.tutee.user.username
        
    class Meta:
        permissions = (
            ("tutee_permission", "is a tutee"), 
            ("coach_permission", "is a coach"),
            ("admin_permission", "is an admin"),
        )
        
class ReassignNote(models.Model):
    project = models.OneToOneField(Project, related_name = 'reassigned_note')
    details = models.TextField(blank=True)
    coach = models.ForeignKey(CoachUser, related_name = 'reassigned_note')
        
class ProjectForm(forms.Form):
    title = forms.CharField()
    details = forms.CharField(widget=forms.Textarea)
    date_of_interest = forms.DateField()
    
class SubmitProjectForm(forms.Form):
    video = forms.FileField(required = False) ##FOR NOW MUST CHANGE!!
    meeting_details = forms.CharField(widget=forms.Textarea)
    meeting_duration = forms.IntegerField()
    meeting_date = forms.DateField()    
    
class CoachUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField(max_length=11)
    ee_help = forms.BooleanField(required = False,label = "Can support EE-focus")
    cs_help = forms.BooleanField(required = False,label = "Can support CS-focus")
    
class TuteeUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput({ "placeholder": "jsmith2013" }))
    password = forms.CharField(widget=forms.TextInput({ "placeholder": "password123" }))
    first_name = forms.CharField(widget=forms.TextInput({ "placeholder": "Jane" }))
    last_name = forms.CharField(widget=forms.TextInput({ "placeholder": "Smith" }))
    email = forms.EmailField(widget=forms.TextInput({ "placeholder": "jsmith@mit.edu" }))
    phone = forms.CharField(max_length=11, widget=forms.TextInput({ "placeholder": "18005556789" }))
    research_advisor = forms.CharField(widget=forms.TextInput({ "placeholder": "Prof. John Doe" }))
    research_advisor_email = forms.EmailField(widget=forms.TextInput({ "placeholder": "johndoe@mit.edu" }))
    ee_request = forms.BooleanField(required = False, label = "EE-Related Research")
    cs_request = forms.BooleanField(required = False, label = "CS-Related Research")
    area_of_interest = forms.CharField(widget=forms.TextInput({ "placeholder": "Artificial Intelligence" }))
    
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
    
class TuteeUserProfileForm(forms.Form):
    email = forms.EmailField()
    phone = forms.CharField(max_length=11)
    research_advisor = forms.CharField()
    research_advisor_email = forms.EmailField()
    ee_request = forms.BooleanField(required = False, label = "EE-related")
    cs_request = forms.BooleanField(required = False, label = "CS-related")
    area_of_interest = forms.CharField(required = False)

class CoachUserProfileForm(forms.Form):
    email = forms.EmailField()
    phone = forms.CharField(max_length=11)
    ee_help = forms.BooleanField(required = False,label = "Can support EE-focus")
    cs_help = forms.BooleanField(required = False,label = "Can support CS-focus")

class ReportForm(forms.Form):
    subject = forms.CharField(label="Subject")
    message = forms.CharField(widget = forms.Textarea, label="Problem Description")

class WithdrawNoteForm(forms.Form):
    details = forms.CharField(widget = forms.Textarea, label="Reason for withdrawl")

class ReqForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput({ "placeholder": "Jane" }))
    last_name = forms.CharField(widget=forms.TextInput({ "placeholder": "Smith" })) 
    athena_username = forms.CharField(widget=forms.TextInput({ "placeholder": "jsmith2013" }))   #ie. presentation date, date of defense, etc.
    email = forms.EmailField(label="Preferred Email", widget=forms.TextInput({ "placeholder": "jsmith2013@mit.edu" })) 
    phone = forms.CharField(widget=forms.TextInput({ "placeholder": "15005552358" }))
    ee_familiarity = forms.BooleanField(required=False)
    cs_familiarity = forms.BooleanField(required=False)

class ValidateAgreementForm(forms.Form):
    agree = forms.BooleanField(required=True, label="I have read and agree with the terms and conditions outlined above")