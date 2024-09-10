from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import date
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):

    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('employer', 'Employer'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('terminated', 'Terminated'),
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )


    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    fname = models.CharField(max_length=200, blank=True, null=True)
    
    lname = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True, unique=True)
    position=models.CharField(max_length=200, blank=True, null=True)
    account_no = models.CharField(max_length=20, blank=True, null=True) 
    account_name = models.CharField(max_length=200, blank=True, null=True)
    address= models.TextField(null=True, blank=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True) 
    date_of_hire = models.DateField(null=True, blank=True)  
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active') 
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    dob = models.DateField(null=True, blank=True) 
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee') 
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.fname +" "+ self.lname)


class Employer(models.Model):
    user = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        primary_key=True
    )
    
    def __str__(self):
        return str(self.user.fname +" "+ self.user.lname)
    

class Attendance(models.Model):
    employee = models.ForeignKey(Profile, on_delete=models.CASCADE, null= True)
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    
    date = models.DateField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.employee.fname} {self.employee.lname} - {self.date}"
    


class Leave(models.Model):
   
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'

    LEAVE_STATUS = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    employee = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True )
    title = models.CharField(max_length=200, blank=True,null=True)
    reason = models.TextField()
    comment = models.TextField()
    
    status = models.CharField(max_length=10, choices=LEAVE_STATUS, default=PENDING)
    start_date = models.DateField()
    end_date = models.DateField()
    applied_on = models.DateField(auto_now_add=True)

    def __str__(self):
         return f"{self.employee.fname} {self.employee.lname} | {self.title} leave "
    def get_days(self):
        return (self.end_date - self.start_date).days + 1






class Task(models.Model):

    HIGH = 'High'
    LOW = 'Low'
    MEDIUM = 'Medium'

    PRIORITY_CHOICES= [
        (HIGH, 'High'),
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
    ]

    STATUS_CHOICES=[

        ('Incomplete', 'Incomplete'),
        ('Complete', 'Complete'),
    ]
    task_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    assignee = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='assignee' )
    assigner = models.ForeignKey(Profile, on_delete=models.CASCADE,  null=False, related_name='assigner')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Low')
    feedback = models.TextField(blank=True, null=True)
    start_date = models.DateField(default=date.today)
    deadline = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Incomplete')


    def __str__(self):

        return self.title


