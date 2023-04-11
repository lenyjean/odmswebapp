from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse
from .models import *
from .forms import *
from .utils import *
# Create your views here.
@login_required(login_url='/login')
def homepage(request):
    template_name = 'home/home.html'
    context = {
        "home_state": "background-color: rgba(212, 210, 210, 1);  color: #fff;",
    }
    return render(request, template_name, context)

def login_page(request):
    template_name = 'authentication/login.html'
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        employee_no = request.POST.get('employee_no')
        password = request.POST.get('password')
        print(employee_no, password)
        user = authenticate(request, employee_no=employee_no, password=password)
    
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in successfully.")
            return redirect("home")
           
        else:
            messages.error(request, "Invalid employee no. or password")           
    context = {
        "form": form
    }
    return render(request, template_name, context)

def logout_page(request):
    logout(request)
    return redirect("login")

@login_required(login_url='/login')
def account(request):
    template_name = 'accounts/account_list.html'
    account = User.objects.all().order_by('-date_joined')
    paginator = Paginator(account, 10)
    page_number = request.GET.get('page')
    account = paginator.get_page(page_number)
    context = {
        "account": account,
        "account_state": "background-color: rgba(212, 210, 210, 1);  color: #fff;",
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def add_account(request):
    template_name = 'accounts/add_account.html'
    form = UserForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user_account = form.save(commit=False)
        user_type = request.POST['user_type']
        print(request.POST['user_type'])
        if user_type == "admin":
            user_account.is_admin = True
        elif user_type == "employee":
            user_account.is_employee = True
        user_account.set_password(request.POST.get("password1"))
        user_account.save()
        print("User account saved:", user_account)
        
    context = {
        "form": form
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def view_account(request,pk):
    template_name = 'accounts/view_account.html'
    account = User.objects.filter(id=pk)
    context = {
        "account": account
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def update_account(request, pk):
    template_name = 'accounts/update_account.html'
    account = get_object_or_404(User, id=pk)
    form = UserUpdateForm(request.POST or None, request.FILES or None, instance=account)
    if form.is_valid():
        form.save()
        return redirect('accounts-list')
    context = {
        "form": form,
        "pk": pk
    }
    return render(request, template_name, context)

def delete_account(request,pk):
    account = User.objects.filter(id=pk)
    account.delete()
    return redirect('accounts-list')

@login_required(login_url='/login')
def category(request):
    template_name = 'category/category_list.html'
    category = Category.objects.all().order_by('-created_at')
    paginator = Paginator(category, 10)
    page_number = request.GET.get('page')
    category = paginator.get_page(page_number)
    context = {
        "category": category,
        "category_state": "background-color: rgba(212, 210, 210, 1);  color: #fff;",
        # "breadcrumb": breadcrumb
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def add_category(request):
    template_name = 'category/add_category.html'
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category')
    context = {
        "form": form,
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def update_category(request, pk):
    template_name = 'category/update_category.html'
    category = get_object_or_404(Category, id=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category')
    context = {
        "form": form,
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def delete_category(request, pk):
    category = Category.objects.filter(id=pk)
    category.delete()
    return redirect('category')

@login_required(login_url='/login')
def document(request):
    template_name = 'document/docu_list.html'
    document = Documents.objects.all().order_by('-uploaded_at')
    paginator = Paginator(document, 10)
    page_number = request.GET.get('page')
    document = paginator.get_page(page_number)
    context = {
        "document": document,
        "document_state": "background-color: rgba(212, 210, 210, 1);  color: #fff;",
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def add_docu(request):
    template_name = 'document/add_docs.html'
    form = DocumentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.uploaded_by = request.user
        obj.save()
        create_history(
            user = f"{request.user.first_name}, {request.user.last_name}",
            history = f"A new document titled {obj.file_name} was uploaded by {request.user.first_name}, {request.user.last_name}",
            user_image = f"{request.user.profile_picture.url}"    
        )
        return redirect('document')
    context = {
        "form": form,
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def view_docu(request, pk):
    template_name = 'document/view_docu.html'
    document = Documents.objects.filter(id=pk)
    context = {
        "document": document
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def update_docu(request, pk):
    template_name = 'document/update_docu.html'
    document = get_object_or_404(Documents, id=pk)
    form = DocumentForm(request.POST or None, instance=document)
    if form.is_valid():
        form.save()
        return redirect('document')
    context = {
        "form": form,
    }
    return render(request, template_name, context)


@login_required(login_url='/login')
def delete_docu(request, pk):
    file = Documents.objects.get(id=pk)
    delete_history(
        user=f"{request.user.first_name}, {request.user.last_name}",
        history=f"The document titled {file.file_name} was deleted by {request.user.first_name}, {request.user.last_name} ",
        user_image = f"{request.user.profile_picture.url}"
    )
    file.delete()
    return redirect('document')

@login_required(login_url='/login')
def history(request):
    template_name = 'history/history_list.html'
    history = ActivityHistory.objects.all().order_by('-created_at')
    paginator = Paginator(history, 10)
    page_number = request.GET.get('page')
    history = paginator.get_page(page_number)
    context = {
        "history": history,
        "history_state": "background-color: rgba(212, 210, 210, 1);  color: #fff;",
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def view_profile(request):
    pk = request.user.id
    template_name = 'accounts/profile/view_profile.html'
    user_data = User.objects.filter(id=request.user.id)
    context = {
        "user_data": user_data,
        "pk": pk
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def password_update(request):
    template_name = 'accounts/profile/update_password.html'
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if new_password != confirm_password:
            messages.error(request, "Passwords doesn't match")
        else:
            try:
                user = User.objects.get(id=request.user.id)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been changed successfully.')
                return redirect("/")
            except User.DoesNotExist:
                messages.error(request, "User doesn't exists")
    context = {
        "pk": request.user.id
    }
    return render(request, template_name, context)