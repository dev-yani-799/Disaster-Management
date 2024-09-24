from django.contrib import admin
from .models import State, Volunteer, EndUser, Alert, Needs, StateCommittee, User, Certificate


# Register your models here.

admin.site.register(User)
admin.site.register(State)
admin.site.register(Volunteer)
admin.site.register(EndUser)
admin.site.register(Alert)
admin.site.register(Needs)
admin.site.register(StateCommittee)
admin.site.register(Certificate)

