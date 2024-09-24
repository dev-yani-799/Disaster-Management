from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    user_type = models.IntegerField(null=True) # 0: Admin || 1:state committee || 2: Volunteer  || 3: user

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class State(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return self.name


class StateCommittee(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.BigIntegerField( null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE, null=True)
    location = models.TextField(null=True) 
    latitude = models.TextField(null=True)
    longitude = models.TextField(null=True)



    def __str__(self) -> str:
        return self.name


class Volunteer(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.BigIntegerField(null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE, null=True)
    location = models.TextField(null=True)
    latitude = models.TextField(null=True)
    longitude = models.TextField(null=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='volunteer_user', null=True)

    def __str__(self) -> str:
        return self.name
        


class EndUser(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.BigIntegerField(null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    location = models.TextField(null=True)
    latitude = models.TextField(null=True)
    longitude = models.TextField(null=True)

    def __str__(self) -> str:
        return self.name


class Alert(models.Model):
    host = models.ForeignKey(EndUser , on_delete=models.CASCADE,null=True)
    state_committee = models.ForeignKey(StateCommittee, on_delete=models.CASCADE, null=True)
    content = models.TextField(max_length=200, null=True)
    status = models.IntegerField(default=0) # 0: pending || 1: open || 2: closed  
    is_verified_by_state = models.IntegerField(default=0) # 0:pending || 1:approved || 2:rejected
    is_verified_by_admin = models.IntegerField(default=0) # 0:pending || 1:approved || 2:rejected
    rejected_by = models.IntegerField(null=True, blank=True) #  0:admin || 1:state || 2:volunteer
    created = models.DateTimeField(auto_now_add=True)
    updated =models.DateTimeField(auto_now=True)
    latitude = models.FloatField(null=True)  # Field to store latitude
    longitude = models.FloatField(null=True)  # Field to store longitude

    class Meta:
        ordering = ['-created', '-updated']

    def __str__(self):
        return f"Alert {self.id}" 



class Needs(models.Model):
    host = models.ForeignKey(Volunteer, on_delete=models.CASCADE, null=True)
    state_committee = models.ForeignKey(StateCommittee, on_delete=models.CASCADE, null=True)
    requirements = models.TextField(null=True)
    status = models.IntegerField(default=0)  # 0:pending || 1:open || 2:closed
    is_verified_by_state = models.IntegerField(default=0) # 0:pending || 1:approved || 2:rejected
    is_verified_by_admin = models.IntegerField(default=0) # 0:pending || 1:approved || 2:rejected
    rejected_by = models.IntegerField(null=True, blank=True) #  0:admin || 1:state || 2:volunteer
    created = models.DateTimeField(auto_now_add=True)
    updated =models.DateTimeField(auto_now=True)
    cr_status =models.IntegerField(default=0)
    
    class Meta:
        ordering =['-updated', '-created']

    def __str__(self) -> str:
        return self.requirements
    

class Certificate(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, null=True)
    need = models.ForeignKey(Needs, on_delete=models.CASCADE, null=True)
    estimate = models.ImageField(upload_to='certificates', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    amount = models.BigIntegerField(null=True)
    status = models.IntegerField(default=0)

    class Meta:
        ordering =['-updated', '-created']

    def __str__(self) -> str:
        return self.volunteer.name
class Complaint(models.Model):
    compaint=models.CharField(max_length=255, null=True)
    userid = models.ForeignKey(User,on_delete=models.CASCADE, null=True)

class EstimateCost(models.Model):
    amount=models.CharField(max_length=255, null=True)
    userid = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    bill = models.ImageField(upload_to='certificates', null=True, blank=True)
    status = models.IntegerField(default=0) # 0: pending || 1: approve 
class UserClaim(models.Model):
    claimname =  models.CharField(max_length=255, null=True)
    address =  models.CharField(max_length=255, null=True)
    claimtype =  models.CharField(max_length=255, null=True)
    description =  models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='certificates', null=True, blank=True)
    userid = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    status = models.IntegerField(default=0) # 0: pending || 1: approve 
class Task_voluenteer(models.Model):
    alertid = models.ForeignKey(Alert,on_delete=models.CASCADE, null=True)   
    volunteerid = models.ForeignKey(Volunteer,on_delete=models.CASCADE, null=True) 
    userid =models.ForeignKey(User,on_delete=models.CASCADE, null=True) 
    taskdescriprion = models.CharField(max_length=255, null=True)
    
    
    
    
    
    



    

