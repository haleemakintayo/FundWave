from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class UserRegistrationModels(AbstractUser):
#   def __str__(self):
#     return self.firstname
  
#   groups = models.ManyToManyField(Group, related_name='userRegistrationModels')
#   user_permissions = models.ManyToManyField(Permission, related_name='userRegistrationModels_Permission')

class UserProfile(models.Model): 
  ACCOUNT_TYPES = (
    ('creator', 'Campaign Creator'),
    ('donator', 'Donator'),
  )

  user = models.OneToOneField(User, on_delete=models.CASCADE)
  account_type= models.CharField(max_length=10, choices=ACCOUNT_TYPES)

  def __str__(self):
    return f"{self.user.first_name} - {self.account_type}"