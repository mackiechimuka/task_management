from django.contrib import admin
from .models import Task
#from users.models import User
from django.contrib.auth.models import User

admin.site.register(Task)