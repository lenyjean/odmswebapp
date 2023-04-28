from django import forms
from .models import *

from django.core.exceptions import ValidationError

# This is a Django form class for the Category model that includes all fields.
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


# The DepartmentForm class is a model form in Django used for creating and updating department
# objects.
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class DocumentForm(forms.ModelForm):
    document = forms.FileField(
        label='Select a PDF file',
        required=True,
        widget=forms.ClearableFileInput(attrs={'accept': 'application/pdf'})
    )

    class Meta:
        model = Documents
        fields = ['file_name', 'category', 'document']

    def clean_document(self):
        document = self.cleaned_data['document']
        if not document.name.endswith('.pdf'):
            raise ValidationError("Only PDF files are allowed.")
        return document

# The `ForwardDocumentForm` class is a ModelForm that allows users to select a recipient department
# for a `Documents` model instance.
class ForwardDocumentForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(label="Select recipient: ", queryset=Department.objects.all())
    class Meta:
        model = Documents
        fields = ['receiver']


# The class defines a form for creating a user with fields for profile picture, user type, employee
# number, first and last name, address, contact number, and password.
user_type = (
    ('admin', 'admin'),
    ('employee', 'employee'),
)
class UserForm(forms.ModelForm):
    user_type = forms.ChoiceField(label="This account is for : ", choices=user_type)
    password = forms.CharField(widget=forms.PasswordInput)
    contact = forms.CharField(label="Contact Number ")
    class Meta:
        model = User
        fields = ['profile_picture', 'user_type', 'employee_no', 'first_name', 'last_name',  'address', 'contact', 'password'] 


# This is a Django form for updating user information including profile picture, name, sex, birthday,
# address, and contact.
class UserUpdateForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=user_type)
    employee_no = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ['profile_picture', 'employee_no', 'first_name', 'last_name', 'sex', 'birthday', 'address', 'contact'] 

# This is a login form class in Python that includes fields for employee number and password.
class LoginForm(forms.Form):
    employee_no = forms.CharField(label='Employee No')
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class" : "form-control"}),
    )
 
    class Meta:
        fields = ['employee_no', 'password']