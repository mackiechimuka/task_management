from django.db import models
#from users.models import User
from django.contrib.auth.models import User



# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=350)
    description = models.TextField()
    allocated_to = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=False,related_name='tasks_allocated')
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
