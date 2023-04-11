from django import forms
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ['file_name', 'category', 'document']

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

class UserUpdateForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=user_type)
    employee_no = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ['profile_picture', 'employee_no', 'first_name', 'last_name', 'sex', 'birthday', 'address', 'contact'] 

class LoginForm(forms.Form):
    employee_no = forms.CharField(label='Employee No')
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class" : "form-control"}),
    )
 
    class Meta:
        fields = ['employee_no', 'password']