from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _



"""
Need to store password as hash, this can be done through the custom user manager after I implement it.
"""

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, role, first_name, last_name, 
                    desk_id, gender, birth_date, nationality, remote_percentage,
                    **other_fields):

        if not email:
            raise ValueError(_('Users must have an email address.'))
        if not password:
            raise ValueError(_('Users must have a password.'))
        if not role:
            raise ValueError(_('Users must have Employee, Admin or Office Admin role.'))
        if not first_name:
            raise ValueError(_('Users must have a first name.'))
        if not last_name:
            raise ValueError(_('Users must have a last name.'))
  
        user = self.model(
            email=self.normalize_email(email),
            role=role,
            first_name=first_name,
            last_name=last_name,
            desk_id=int(desk_id),
            gender=gender,
            birth_date=birth_date,
            nationality=nationality, 
            remote_percentage=remote_percentage,
            **other_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, role, first_name, last_name, 
                         desk_id, gender, birth_date, nationality, remote_percentage,
                         **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        
        return self.create_user(email, password, role, first_name, last_name, desk_id, 
                                gender, birth_date, nationality, remote_percentage, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):

    class UserObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_active=True)


    ADMIN = 'Admin'
    OFFICE_ADMIN = 'Office Admin'
    EMPLOYEE = 'Employee'

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    NONE = 'N'

    USER_TYPE_CHOICES = [
        (ADMIN, 'Admin'),
        (OFFICE_ADMIN, 'Office Admin'),
        (EMPLOYEE, 'Employee'),
    ]

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        (NONE, 'None')
    ]
    
    email = models.EmailField(max_length=200, null=False, blank=False, unique=True)
    password = models.CharField(max_length=200, null=False, blank=False)
    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    role = models.CharField(max_length=200, choices=USER_TYPE_CHOICES, default=EMPLOYEE, null=False, blank=False)
    desk_id = models.OneToOneField('Desk', on_delete=models.SET_NULL, null=True, blank=True, default=None,
                                    db_column='desk_id')
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=200, blank=True)
    remote_percentage = models.FloatField(default=0, null=False, blank=True,
                                          validators=[
                                              MaxValueValidator(100),
                                              MinValueValidator(0)
                                          ])
    is_active = models.BooleanField(default=False, null=False, blank=False)
    is_staff = models.BooleanField(default=False, null=False, blank=False)
    is_superuser = models.BooleanField(default=False, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'role', 'first_name', 'last_name', 'desk_id', 'gender', 'birth_date', 'nationality', 'remote_percentage']

    objects = CustomUserManager() # custom permission manager
    userObjects = UserObjects() # custom manager
    

    class Meta:
        ordering = ('role',)

    def __str__(self):
        return self.email


class Remote_Request(models.Model):

    PENDING = 'P'
    APPROVED = 'A'
    REJECTED = 'R'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, db_column='user_id')
    remote_percentage = models.FloatField(default=0, null=False, blank=False,
                                          validators=[
                                              MaxValueValidator(100),
                                              MinValueValidator(0)
                                          ])
    request_reason = models.TextField(null=False, blank=False)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES, default=PENDING, null=False, blank=False)
    reject_reason = models.TextField(blank=True)


class Desk_Request(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, 
                                db_column='user_id')
    office_id = models.ForeignKey('Office', on_delete=models.CASCADE, null=False, blank=False, 
                                  db_column='office_id')
    request_reason = models.TextField(blank=False)


    PENDING = 'P'
    APPROVED = 'A'
    REJECTED = 'R'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')
    ]

    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=PENDING, null=False, blank=True)
    reject_reason = models.TextField(blank=True)


class Building(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    floors_count = models.PositiveIntegerField(null=False, blank=False)
    building_address = models.CharField(max_length=200, null=False, blank=False)


class Office(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    building_id = models.ForeignKey('Building', on_delete=models.CASCADE, null=False, blank=False, 
                                    db_column='building_id')
    floor_number = models.PositiveIntegerField(null=False, blank=False)
    total_desks = models.PositiveIntegerField(null=False, blank=False, default=0)
    usable_desks = models.PositiveIntegerField(null=False, blank=False, default=0)
    

    office_admin_id = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                           db_column='office_admin_id')


class Desk(models.Model):
    desk_number = models.PositiveIntegerField(null=False, blank=False)
    office_id = models.ForeignKey('Office', on_delete=models.CASCADE, null=False, blank=False, 
                                  db_column='office_id')
    is_usable = models.BooleanField(default=True)


class Office_Image(models.Model):
    office_id = models.ForeignKey('Office', on_delete=models.CASCADE, null=False, blank=False, 
                                  db_column='office_id')
    img_url = models.CharField(max_length=200, null=False, blank=False)


class User_Image(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False, 
                                db_column='user_id')
    img_url = models.CharField(max_length=200, null=False, blank=False)
