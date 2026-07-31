from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employees')
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('On Leave', 'On Leave'),
        ('Remote', 'Remote'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default='Staff Member')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    phone = models.CharField(max_length=20, blank=True, default='+1 415 555-0100')
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    joining_date = models.DateField()
    
    def __str__(self):
        return self.name

    @property
    def emp_id_formatted(self):
        return f"KE-{self.id:05d}"