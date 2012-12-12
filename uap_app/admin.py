from django.contrib import admin
from uap_app.models import *

admin.site.register(TuteeUser)
admin.site.register(CoachUser)
admin.site.register(CoachRequest)
admin.site.register(Ticket)
admin.site.register(TicketNote)