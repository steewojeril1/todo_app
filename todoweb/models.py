from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #mandatory#ensures that if a user is deleted, all their todos are also deleted
    title = models.CharField(max_length=255)  #mandatory
    completed = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True) #automatically set


    def __str__(self):
        return self.title    
