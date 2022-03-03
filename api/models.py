from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=200, null=False, blank=False)
    password = models.CharField(max_length=200, null=False, blank=False)
    desk = models.OneToOneField('Desks', on_delete=models.SET_NULL, null=True, blank=True)


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


class Remote_Requests(models.Model):
    id = models.BigAutoField(primary_key=True)
    employee = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
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


class Desk_Requests(models.Model):
    id = models.BigAutoField(primary_key=True)
    employee = models.ForeignKey(Users, on_delete=models.CASCADE)
    office = models.ForeignKey('Offices', on_delete=models.CASCADE)
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


class Buildings(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    floors_count = models.PositiveIntegerField(null=False, blank=False)
    building_address = models.CharField(max_length=200, null=False, blank=False)

    # list of office id's that are in this building
    office = models.ForeignKey('Offices', on_delete=models.CASCADE, null=True, blank=True)


class Offices(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    office_address = models.CharField(max_length=200, null=False, blank=False)
    building = models.ForeignKey('Buildings', on_delete=models.CASCADE, null=False, blank=False)
    floor_number = models.PositiveIntegerField(null=False, blank=False)
    
    width_meters = models.FloatField(null=False, blank=False)
    length_meters = models.FloatField(null=False, blank=False)

    office_admin = models.OneToOneField(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='office_admin')
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    # list of all the desks in this office
    desk = models.ForeignKey('Desks', on_delete=models.CASCADE, null=True, blank=True)

    # list of images id's related to this office
    office_images = models.ForeignKey('Images', on_delete=models.SET_NULL, null=True, blank=True)


class Desks(models.Model):
    id = models.BigAutoField(primary_key=True)
    desk_number = models.PositiveIntegerField(null=False, blank=False)
    office = models.ForeignKey('Offices', on_delete=models.CASCADE)
    assigned_employee = models.OneToOneField(Users, on_delete=models.CASCADE, null=True, blank=True)
    is_usable = models.BooleanField(default=True)
    width_cm = models.PositiveIntegerField(null=False, blank=False)
    height_cm = models.PositiveIntegerField(null=False, blank=False)


class Images(models.Model):
    id = models.BigAutoField(primary_key=True)
    office = models.ForeignKey('Offices', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=200, null=False, blank=False)
