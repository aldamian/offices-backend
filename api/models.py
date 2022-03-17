from re import T
from datetime import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, role, first_name, last_name, office_id, building_id, 
                    gender, birth_date, nationality, remote_percentage, 
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
        if nationality != '' or nationality != 'None':
            nationality=nationality.capitalize()
        if birth_date:
            present=datetime.now()
            if birth_date > present.date():
                raise ValueError(_("Can't select a future date."))
        
        
        try: 
            int(office_id) 
            office_id = Office.objects.get(pk=office_id)
        except ValueError:
            office_id = None
        except TypeError:
            office_id = None

        try:
            int(building_id)
            building_id = Building.objects.get(pk=building_id)
        except ValueError:
            building_id = None
        except TypeError:
            building_id = None

        user = self.model(
            email=self.normalize_email(email),
            role=role.capitalize(),
            first_name=first_name.capitalize(),
            last_name=last_name.capitalize(),
            office_id=office_id,
            building_id=building_id,
            gender=gender,
            birth_date=birth_date,
            nationality=nationality, 
            remote_percentage=remote_percentage,
            **other_fields
        )
        
        user.set_password(password) # takes care of the hashing
        user.save()
        return user


    def create_superuser(self, email, password, role, first_name, last_name, office_id, building_id, 
                         gender, birth_date, nationality, remote_percentage,
                         **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        
        return self.create_user(email, password, role, first_name, last_name, office_id, building_id, 
                                gender, birth_date, nationality, remote_percentage,
                                **other_fields)


class User(AbstractBaseUser, PermissionsMixin):

    class UserObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_active=True)


    ADMIN = _('Admin')
    OFFICE_ADMIN = _('Office Admin')
    EMPLOYEE = _('Employee')

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'

    USER_TYPE_CHOICES = [
        (ADMIN, _('Admin')),
        (OFFICE_ADMIN, _('Office Admin')),
        (EMPLOYEE, _('Employee')),
    ]

    GENDER_CHOICES = [
        (MALE, _('Male')),
        (FEMALE, _('Female')),
        (OTHER, _('Other')),
    ]
    
    email = models.EmailField(max_length=200, null=False, blank=False, unique=True)
    password = models.CharField(max_length=200, null=False, blank=False)
    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    role = models.CharField(max_length=200, choices=USER_TYPE_CHOICES, 
                            default=EMPLOYEE, null=False, blank=False)
    office_id = models.ForeignKey('Office', on_delete=models.SET_NULL, 
                                  null=True, blank=True, db_column='office_id')
    building_id = models.ForeignKey('Building', on_delete=models.SET_NULL, 
                                    null=True, blank=True, db_column='building_id')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=200, blank=True, default='None')
    remote_percentage = models.FloatField(default=0, null=False, blank=True,
                                          validators=[
                                              MaxValueValidator(100),
                                              MinValueValidator(0)
                                          ])
    img_url = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'role', 'first_name', 'last_name', 'office_id', 'building_id', 
                       'gender', 'birth_date', 'nationality', 'remote_percentage']

    objects = CustomUserManager() # custom permission manager
    userObjects = UserObjects() # custom manager
    

    class Meta:
        ordering = ('role',)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def get_role(self):
        return self.role
    
    def get_desk(self):
        return self.desk_id

    def get_gender(self):
        return self.gender

    def get_birth_date(self):
        return self.birth_date

    def get_nationality(self):
        return self.nationality

    def get_remote_percentage(self):
        return self.remote_percentage

    def get_img_url(self):
        return self.img_url


class Request(models.Model):

    PENDING = 'P'
    APPROVED = 'A'
    REJECTED = 'R'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')
    ]

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                null=False, blank=False, db_column='user_id')
    office_id = models.ForeignKey('Office', on_delete=models.CASCADE,
                                  null=False, blank=False, db_column='office_id')
    remote_percentage = models.FloatField(default=0, null=False, blank=False,
                                          validators=[
                                              MaxValueValidator(100),
                                              MinValueValidator(0)
                                          ])
    request_reason = models.TextField(null=False, blank=False)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES, default=PENDING, 
                              null=False, blank=False)
    reject_reason = models.TextField(blank=True, default='Request denied.')

    def __str__(self):
        return str(self.user_id)

    def get_user_id(self):
        return self.user_id

    def get_office_id(self):
        return self.office_id
    
    def get_remote_percentage(self):
        return self.remote_percentage

    def get_request_reason(self):
        return self.request_reason

    def get_status(self):
        return self.status

    def get_reject_reason(self):
        return self.reject_reason


class Building(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    floors_count = models.PositiveIntegerField(null=False, blank=False)
    address = models.CharField(max_length=200, null=False, blank=False, unique=True)
    img_url = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    def get_floors_count(self):
        return self.floors_count

    def get_building_address(self):
        return self.address


class Office(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    building_id = models.ForeignKey('Building', on_delete=models.CASCADE, null=False, blank=False, 
                                    db_column='building_id')
    floor_number = models.PositiveIntegerField(null=False, blank=False)
    total_desks = models.PositiveIntegerField(null=False, blank=False)
    usable_desks = models.PositiveIntegerField(null=False, blank=False)
    x_size_m = models.FloatField(null=False, blank=False, default=0.0)
    y_size_m = models.FloatField(null=False, blank=False, default=0.0)

    # array of desk ids
    desk_ids = ArrayField(models.PositiveIntegerField(), null = True, blank=True)

    office_admin= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, 
                                           db_column='office_admin_id')

    def __str__(self):
        return self.name

    def get_building_id(self):
        return self.building_id

    def get_floor_number(self):
        return self.floor_number

    def get_total_desks(self):
        return self.total_desks

    def get_usable_desks(self):
        return self.usable_desks

    def get_office_admin_id(self):
        return self.office_admin_id


class Desk(models.Model):
    office_id = models.ForeignKey('Office', on_delete=models.CASCADE, null=False, blank=False, 
                                  db_column='office_id') # [null] means that request is remote
    desk_number = models.PositiveIntegerField(null=False, blank=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                null=True, blank=True, db_column='user_id')
    x_size_m = models.FloatField(null=False, blank=False, default=0.0)
    y_size_m = models.FloatField(null=False, blank=False, default=0.0)
    x_pos_px = models.PositiveIntegerField(null=False, blank=False, default=0)
    y_pos_px = models.PositiveIntegerField(null=False, blank=False, default=0)
    is_usable = models.BooleanField(default=True)

    def __str__(self):
        return str(self.desk_number)

    def get_office_id(self):
        return self.office_id

    def get_user_id(self):
        return self.user_id

    def get_is_usable(self):
        return self.is_usable



class Office_Image(models.Model):
    office_id = models.ForeignKey('Office', on_delete=models.CASCADE, null=False, blank=False, 
                                  db_column='office_id')
    img_url = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return str(self.office_id)

    def get_img_url(self):
        return self.img_url

