from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator


class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True, db_column='id')
    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=200, null=False, blank=False, unique=True)
    password = models.CharField(max_length=200, null=False, blank=False)
    desk_id = models.OneToOneField('Desk', on_delete=models.SET_NULL, null=True, blank=True, db_column='desk_id')
    

    ADMIN = 'Admin'
    OFFICE_ADMIN = 'Office Admin'
    EMPLOYEE = 'Employee'
    USER_TYPE_CHOICES = [
        (ADMIN, 'Admin'),
        (OFFICE_ADMIN, 'Office Admin'),
        (EMPLOYEE, 'Employee'),
    ]

    role = models.CharField(max_length=200, choices=USER_TYPE_CHOICES, default=EMPLOYEE)

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other')
    ]

    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)

    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=200, null=True, blank=True)
    remote_percentage = models.FloatField(default=0,
                                          validators=[
                                              MaxValueValidator(100),
                                              MinValueValidator(0)
                                          ])
    is_deactivated = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password', 'role']


class Remote_Request(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, db_column='user_id')
    remote_percentage = models.FloatField(default=0,
                                          validators=[
                                              MaxValueValidator(100),
                                              MinValueValidator(0)
                                          ])
    request_reason = models.TextField(null=False, blank=False)


    PENDING = 'P'
    APPROVED = 'A'
    REJECTED = 'R'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')
    ]

    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=PENDING)

    reject_reason = models.TextField(null=True, blank=True)


class Desk_Request(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, db_column='user_id')
    office = models.ForeignKey('Office', on_delete=models.CASCADE)
    request_reason = models.TextField(null=False, blank=False)


    PENDING = 'P'
    APPROVED = 'A'
    REJECTED = 'R'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')
    ]

    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=PENDING)

    reject_reason = models.TextField(null=True, blank=True)


class Building(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=200, null=False, blank=False)
    floors_count = models.PositiveIntegerField(null=False, blank=False)
    building_address = models.CharField(max_length=200, null=False, blank=False)

    # list of office id's that are in this building
    office_id = models.ForeignKey('Office', on_delete=models.CASCADE, null=True, blank=True, db_column='office_id')


class Office(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=200, null=False, blank=False)
    office_address = models.CharField(max_length=200, null=False, blank=False)
    building_id = models.ForeignKey('Building', on_delete=models.CASCADE, null=False, blank=False, db_column='building_id')
    floor_number = models.PositiveIntegerField(null=False, blank=False)
    

    office_admin = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='office_admin', db_column='office_admin_id')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user', db_column='user_id')

    # list of all the desks in this office
    desk_id = models.ForeignKey('Desk', on_delete=models.CASCADE, null=True, blank=True, db_column='desk_id')

    # list of images id's related to this office
    img_id = models.ForeignKey('Image', on_delete=models.SET_NULL, null=True, blank=True, db_column='img_id')


class Desk(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    desk_number = models.PositiveIntegerField(null=False, blank=False)
    office_id = models.ForeignKey('Office', on_delete=models.CASCADE, null=False, blank=False, db_column='office_id')
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='assigned_employee', db_column='employee_id')
    is_usable = models.BooleanField(default=True)


class Image(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    office_id = models.ForeignKey('Office', on_delete=models.CASCADE, null=False, blank=False, db_column='office_id')
    image_url = models.CharField(max_length=200, null=False, blank=False)
