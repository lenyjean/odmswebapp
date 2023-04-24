from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

import uuid

def_uuid = uuid.uuid4()
gen_uuid = str(def_uuid)[:6]
# Create your models here.
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


class User(AbstractUser):

    USERNAME_FIELD = 'employee_no'# changes email to unique and blank to false
    REQUIRED_FIELDS = []  # removes email from REQUIRED_FIELDS
    username = models.CharField(max_length=255, null=True, blank=True)
    employee_no = models.CharField(max_length=255, unique=True)
    profile_picture = models.ImageField(upload_to="profile_picture", default='default.png')
    middle_name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255)
    birthday = models.DateField(auto_now_add=False, null=True, blank=True)
    contact = models.CharField(max_length=255)
    sex = models.CharField(max_length=255)
    is_employee = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.first_name + " " + self.last_name
    
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category
    
class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.department

class Documents(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tracking_no = models.CharField(max_length=255, default=f"DOC-{gen_uuid}", editable=False)
    file_name = models.CharField(max_length=255)
    document = models.FileField(upload_to="documents")
    receiver = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="file_uploader")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="file_category")

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return self.file_name 

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
