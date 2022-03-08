from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, first_name, last_name, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(email, first_name, last_name, password, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
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
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password', 'role']
    objects = CustomUserManager()

    def __str__(self):
        return self.email


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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, 
                                db_column='user_id')
    # replace with office name?
    office_id = models.ForeignKey('Office', on_delete=models.CASCADE, null=False, blank=False, 
                                  db_column='office_id')
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


class Office(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=200, null=False, blank=False)
    building_id = models.ForeignKey('Building', on_delete=models.CASCADE, null=False, blank=False, 
                                    db_column='building_id')
    floor_number = models.PositiveIntegerField(null=False, blank=False)
    total_desks = models.PositiveIntegerField(null=False, blank=False, default=0)
    usable_desks = models.PositiveIntegerField(null=False, blank=False, default=0)
    

    office_admin_id = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                           db_column='office_admin_id')


class Desk(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    desk_number = models.PositiveIntegerField(null=False, blank=False)
    office_id = models.ForeignKey('Office', on_delete=models.CASCADE, null=False, blank=False, 
                                  db_column='office_id')
    is_usable = models.BooleanField(default=True)


class Image(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    office_id = models.ForeignKey('Office', on_delete=models.CASCADE, null=False, blank=False, 
                                  db_column='office_id')
    img_url = models.CharField(max_length=200, null=False, blank=False)
