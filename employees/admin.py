from django.contrib import admin
from .models import Profile, Employer, Attendance,Leave, Task


# Register your models here.
admin.site.register(Profile)
admin.site.register(Employer)
admin.site.register(Attendance)
admin.site.register(Leave)
admin.site.register(Task)