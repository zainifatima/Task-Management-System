from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    
     STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
     SECTION_CHOICES = [
        ('software', 'Software'),
        ('networking', 'Networking'),
        ('it', 'IT'),
    ]

    #  PRIORITY_CHOICES = [
    #     ('low', 'Low'),
    #     ('medium', 'Medium'),
    #     ('high', 'High'),
    # ]

     title = models.CharField(max_length=100, null=True, blank=True)
     status = models.CharField(max_length=100,choices=STATUS_CHOICES, default='pending', null=True, blank=True)
     section= models.CharField(max_length=100, null=True, blank=False) 
     priority = models.CharField(max_length=100, null=True, blank=True)
    #  time =models.TimeField(max_length=100, null=True, blank=True)
    #  date = models.DateField(blank=True, null=True)
    #  entry_date = models.DateTimeField(auto_now_add=True)
     desc =  models.CharField(max_length=250, null=True, blank=True)
     assign_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', blank=True, null=True)
     created_at = models.DateTimeField(auto_now_add=True,auto_now=False,blank=True, null=True)
     def __str__(self):
      return self.title     

# class Section(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     admin = models.ForeignKey(User, on_delete=models.CASCADE)
#     def __str__(self):
#       return self.name

# Create groups for each section
# software_group, created = Group.objects.get_or_create(name='Software Admins')
# networking_group, created = Group.objects.get_or_create(name='Networking Admins')
# it_group, created = Group.objects.get_or_create(name='IT Admins')