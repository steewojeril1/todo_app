from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.contrib.auth import get_user_model # this will return value in AUTH_USER_MODEL in settings

#Use a custom user model (by extending AbstractUser) only at the start of a project.
# If migrations are already applied and the default User model is used throughout the project, it's better to create a new UserProfile model instead of switching the user model later."
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True) # blank - Field is allowed to be empty in forms # null - Field is allowed to store NULL in the database
    address = models.TextField(blank=True, null=True)

class Todo(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Use this to support custom or default User models
    #mandatory#ensures that if a user is deleted, all their todos are also deleted
    title = models.CharField(max_length=255)  #mandatory
    completed = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True) #automatically set


    def __str__(self):
        return self.title    
