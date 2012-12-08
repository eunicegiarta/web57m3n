### pre-populate db with some dummy stuff ###
from models import *
import datetime

def create_coaches():
    coach1 = User(username = "coach1", is_active=True)
    coach1.set_password='pwcoach'
    coach1.first_name = "first"
    coach1.last_name = "last"
    coach1.email = 'coach1@yahoo.com'
    coach1.save()
    print "created USER"
    c1 = CoachUser()
    c1.user = coach1
    c1.ee_help = True
    c1.cs_help = True
    c1.projects_assigned = 0
    c1.phone = '18005552323'
    c1.save()
    print 'created COACH'
    
    coach2 = User(username = "coach2", is_active=True)
    coach2.set_password='pwcoach'
    coach2.first_name = "first"
    coach2.last_name = "last"
    coach2.email = 'coach2@yahoo.com'
    coach2.save()
    print "created USER"
    c2 = CoachUser()
    c2.user = coach2
    c2.ee_help = True
    c2.cs_help = True
    c2.projects_assigned = 0
    c2.phone = '18005554327'
    c2.save()
    print 'created COACH'
    
    coach2 = User(username = "coach3", is_active=True)
    coach2.set_password='pwcoach'
    coach2.first_name = "first"
    coach2.last_name = "last"
    coach2.email = 'coach2@yahoo.com'
    coach2.save()
    print "created USER"
    c2 = CoachUser()
    c2.user = coach2
    c2.ee_help = True
    c2.cs_help = True
    c2.projects_assigned = 0
    c2.phone = '18005554327'
    c2.save()
    print 'created COACH'
    
def create_tutees():
    tut1 = User.objects.create_user(username = "tutee1", password='pwt')
    tut1.first_name = "first"
    tut1.last_name = "last"
    tut1.email = 'tutee1@yahoo.com'
    tut1.save()
    print "created USER"
    c1 = TuteeUser()
    c1.user = tut1
    c1.ee_request = True
    c1.cs_request = False
    c1.open_project = False
    c1.area_of_interest = 'robotics'
    c1.research_advisor = 'LK'
    c1.research_advisor_email = 'lk@yahoo.com'
    c1.phone = '180055524345'
    c1.save()
    print 'created TUTEE'
    
    tut2 = User.objects.create_user(username = "tutee2", password='pwt')
    tut2.first_name = "first"
    tut2.last_name = "last"
    tut2.email = 'tutee2@yahoo.com'
    tut2.save()
    print "created USER"
    c2 = TuteeUser()
    c2.user = tut2
    c2.ee_request = True
    c2.cs_request = True
    c2.open_project = True
    c2.area_of_interest = 'robotics'
    c2.research_advisor = 'LK'
    c2.research_advisor_email = 'lk@yahoo.com'
    c2.phone = '180054524345'
    c2.save()
    print 'created TUTEE'
    
    tut2 = User.objects.create_user(username = "tutee3", password='pwt')
    tut2.save()
    tut2.first_name = "first"
    tut2.last_name = "last"
    tut2.email = 'tutee2@yahoo.com'
    tut2.save()
    print "created USER"
    c2 = TuteeUser()
    c2.user = tut2
    c2.ee_request = False
    c2.cs_request = True
    c2.open_project = True
    c2.area_of_interest = 'robotics'
    c2.research_advisor = 'LK'
    c2.research_advisor_email = 'lk@yahoo.com'
    c2.phone = '180054524345'
    c2.save()
    print 'created TUTEE'
    
def create_admins():
    ad1 = User(username = "admin1", is_active=True)
    ad1.set_password('pwt')
    ad1.first_name = "first"
    ad1.last_name = "last"
    ad1.email = 'admin1@yahoo.com'
    ad1.save()
    print "created USER"
    a = AdminUser()
    a.user = ad1
    a.save()
    print 'created ADMIN'
    
def create_projects():
    p = Project()
    p.tutee = TuteeUser.objects.get(id=2)
    p.title = 'some cool thing'
    p.description = 'still in the works'
    p.status = 1
    p.date_of_interest = datetime.datetime(2013,01,01)
    p.save()
    
    p = Project()
    p.tutee = TuteeUser.objects.get(id=1)
    p.title = 'some cool thing2'
    p.description = 'still in the works2'
    p.status = 1
    p.date_of_interest = datetime.datetime(2013,01,01)
    p.save()
    
    p = Project()
    p.tutee = TuteeUser.objects.get(id=3)
    p.title = 'some cool thing3'
    p.description = 'still in the works3'
    p.status = 3
    p.coach = CoachUser.objects.get(id=1)
    p.date_of_interest = datetime.datetime(2013,01,01)
    p.save()
    
    

def delete_users():
    if (User.objects.all()):
        User.objects.all().delete()
        
def delete_projects():
    if (Project.objects.all()):
        Project.objects.all().delete()