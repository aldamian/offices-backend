from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, role, first_name, last_name, **other_fields):

        if not email:
            raise ValueError('Users must have an email address.')
        if not first_name:
            raise ValueError('Users must have a first name.')
        if not last_name:
            raise ValueError('Users must have a last name.')

        other_fields.setdefault('desk_id', None)
        other_fields.setdefault('gender', None)
        other_fields.setdefault('birth_date', None)
        other_fields.setdefault('nationality', None)
        other_fields.setdefault('remote_percentage', 0)

        other_fields.setdefault('is_staff', False)
        other_fields.setdefault('is_superuser', False)
        other_fields.setdefault('is_active', True)
        
        user = self.model(
            email=self.normalize_email(email),
            role=role,
            first_name=first_name,
            last_name=last_name,
            **other_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, role, first_name, last_name, 
                         desk_id, gender, birth_date, nationality, remote_percentage,
                         **other_fields):

        if not email:
            raise ValueError('Superuser must have an email address.')
        if not role:
            raise ValueError('Superuser must have Admin or Office Admin role.')
        if not first_name:
            raise ValueError('Superuser must have a first name.')
        if not last_name:
            raise ValueError('Superuser must have a last name.')

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.model(
            email=self.normalize_email(email),
            role=role,
            first_name=first_name,
            last_name=last_name,
            desk_id=desk_id,
            gender=gender,
            birth_date=birth_date,
            nationality=nationality,
            remote_percentage=remote_percentage
        )

        user.set_password(password)
        


        return user

    
    # return only active users
    class UserObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_active=True)


class User(AbstractBaseUser, PermissionsMixin):


    ADMIN = 'Admin'
    OFFICE_ADMIN = 'Office Admin'
    EMPLOYEE = 'Employee'

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'

    USER_TYPE_CHOICES = [
        (ADMIN, 'Admin'),
        (OFFICE_ADMIN, 'Office Admin'),
        (EMPLOYEE, 'Employee'),
    ]

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other')
    ]
    
    email = models.EmailField(max_length=200, null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    password = models.CharField(max_length=200, null=False, blank=False)
    role = models.CharField(max_length=200, choices=USER_TYPE_CHOICES, default=EMPLOYEE)
    desk_id = models.OneToOneField('Desk', on_delete=models.SET_NULL, null=True, blank=True, 
                                    db_column='desk_id')
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=200, null=True, blank=True)
    remote_percentage = models.FloatField(default=0,
                                          validators=[
                                              MaxValueValidator(100),
                                              MinValueValidator(0)
                                          ])
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password', 'role']
    objects = CustomUserManager() # custom permission manager


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

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, db_column='user_id')
    remote_percentage = models.FloatField(default=0,
                                          validators=[
                                              MaxValueValidator(100),
                                              MinValueValidator(0)
                                          ])
    request_reason = models.TextField(null=False, blank=False)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=PENDING)
    reject_reason = models.TextField(null=True, blank=True)


class Desk_Request(models.Model):
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


class Image(models.Model):
    office_id = models.ForeignKey('Office', on_delete=models.CASCADE, null=False, blank=False, 
                                  db_column='office_id')
    img_url = models.CharField(max_length=200, null=False, blank=False)
