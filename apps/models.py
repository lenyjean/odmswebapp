from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from django.core.validators import RegexValidator

import uuid

def_uuid = uuid.uuid4()
gen_uuid = str(uuid.uuid4())[:6]

phone_regex = RegexValidator(
        regex=r'^\+63\d{10}$',
        message="Phone number must be in the format '+639XXXXXXXXX'"
    )


# Create your models here.
# This is a custom user model manager in Python where email is used as the unique identifier for
# authentication instead of usernames, with methods to create a user and a superuser.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, employee_no, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not employee_no:
            raise ValueError('The Employee No must be set')
        email = self.normalize_email(employee_no)
        user = self.model(employee_no=employee_no, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, employee_no, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(employee_no, password, **extra_fields)


# This is a custom user model in Django with additional fields such as employee number, profile
# picture, middle name, address, birthday, contact, sex, department, and boolean fields for employee
# and admin status.
class User(AbstractUser):

    USERNAME_FIELD = 'employee_no'# changes email to unique and blank to false
    REQUIRED_FIELDS = []  # removes email from REQUIRED_FIELDS
    username = models.CharField(max_length=255, null=True, blank=True)
    employee_no = models.CharField(max_length=255, unique=True)
    profile_picture = models.ImageField(upload_to="profile_picture", default='default.png')
    middle_name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255)
    birthday = models.DateField(auto_now_add=False, null=True, blank=True)
    contact = models.CharField(max_length=13)
    sex = models.CharField(max_length=255)
    is_employee = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()
    department = models.OneToOneField("Department", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.first_name + " " + self.last_name
    
# This is a Django model class for a Category object with fields for id, category name, and creation
# timestamp.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category
    
# This is a Django model class for a Department object with fields for id, department name, and
# creation timestamp.
class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.department

# This is a Django model class for storing documents with fields for tracking number, file name,
# document file, upload and receiver information.
class Documents(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tracking_no = models.CharField(max_length=255, default=str(uuid.uuid4())[:6], editable=False)
    file_name = models.CharField(max_length=255)
    document = models.FileField(upload_to="documents")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="file_uploader")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="file_category")
    is_received = models.BooleanField(default=False)
    receiver = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="file_receiver", verbose_name="Receiving Office:")

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return self.file_name 

# This is a Django model class for storing activity history with fields for user, history, user image,
# and read status.
class ActivityHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=255)
    history = models.CharField(max_length=255)
    user_image = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Activity History'
        verbose_name_plural = 'Activity Histories'

    def __str__(self):
        return self.history


class Notifications(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="created_by_user")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=255)


    def __str__(self):
        return self.message