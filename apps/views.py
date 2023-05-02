from django.http import JsonResponse
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
def login_page(request):
    """
    This function handles the login page, authenticates user credentials, and redirects them to the home
    page if successful.
    
    :param request: The HTTP request object that contains information about the current request, such as
    the user's browser information, the requested URL, and any data submitted in the request
    :return: The function `login_page` returns an HTTP response with the rendered template
    `authentication/login.html` and a context dictionary containing the `form` object. If the request
    method is POST, the function attempts to authenticate the user with the provided `employee_no` and
    `password`. If the authentication is successful, the user is logged in and redirected to the home
    page. If the authentication fails, an error
    """
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
    """
    This function logs out the user and redirects them to the homepage.
    
    :param request: The request parameter is an object that represents the current HTTP request. It
    contains information about the request, such as the URL, headers, and any data submitted in the
    request. In this specific code snippet, the request parameter is used to log out the current user
    and redirect them to the homepage ("/")
    :return: a redirect to the root URL ("/").
    """
    logout(request)
    return redirect("/")

@login_required(login_url='/login')
def homepage(request):
    """
    This function returns a rendered HTML template with a context containing a CSS style for the
    homepage.
    
    :param request: The request object represents the HTTP request that the user made to access the web
    page
    :return: The function `homepage` returns an HTTP response generated by the `render` function, which
    renders the `home.html` template with the given context dictionary. The rendered HTML content is
    sent back to the client as the response.
    """
    template_name = 'home/home.html'
    context = {
        "home_state": "background-color: rgba(212, 210, 210, 1);  color: #fff;",
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def account(request):
    """
    This function retrieves a list of user accounts, paginates them, and renders them in a template.
    
    :param request: The HTTP request object that contains information about the current request, such as
    the user's session and any submitted form data
    :return: The function `account(request)` is returning a rendered HTML template named
    'accounts/account_list.html' with a context dictionary containing a paginated list of User objects
    ordered by date joined, as well as a CSS style for the account state.
    """
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
    """
    This function adds a new user account with the specified user type and password.
    
    :param request: The HTTP request object that contains metadata about the request being made, such as
    the HTTP method, headers, and data
    :return: a rendered HTML template named 'add_account.html' with a context dictionary containing a
    form object.
    """
    template_name = 'accounts/add_account.html'
    form = UserForm(request.POST or None, request.FILES or None)
    department = request.POST.get("department")
    department_name = Department.objects.filter(id=department).first()
    if request.method == 'POST':
        if form.is_valid():
            user_account = form.save(commit=False)
            user_type = request.POST['user_type']
            print(request.POST['user_type'])
            if user_type == "admin":
                user_account.is_admin = True
            elif user_type == "employee":
                user_account.is_employee = True
            user_account.save()
            print("User account saved:", user_account)
        else:
            messages.error(request, f"Error adding new user. Account already exists in {department_name.department}")
            return redirect('/account/add')
    context = {
        "form": form
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def view_account(request,pk):
    """
    This function retrieves a user account with a specific ID and renders a template to display the
    account information.
    
    :param request: The HTTP request object that contains information about the current request, such as
    the user's browser information, the requested URL, and any data submitted in the request
    :param pk: pk stands for "primary key". In this context, it refers to the unique identifier of a
    User object in the database. The view_account function takes a request object and a pk parameter as
    input, and returns a rendered HTML template that displays information about the User object with the
    specified primary key
    :return: The function `view_account` returns an HTTP response with the rendered `view_account.html`
    template, which displays the account information of the user with the specified `pk` (primary key)
    value. The account information is passed to the template through the `context` dictionary.
    """
    template_name = 'accounts/view_account.html'
    account = User.objects.filter(id=pk)
    context = {
        "account": account
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def update_account(request, pk):
    """
    This function updates a user account with the data submitted through a form.
    
    :param request: The HTTP request object that contains information about the current request, such as
    the user making the request, the HTTP method used, and any data submitted with the request
    :param pk: pk stands for "primary key" and it is used to identify a specific record in a database
    table. In this case, it is used to identify a specific user account that needs to be updated
    :return: a rendered HTML template with a form to update a user account. If the form is valid, it
    saves the changes and redirects to the accounts list page. If the form is not valid, it stays on the
    same page and displays the form with errors. The context includes the form and the primary key of
    the user account being updated.
    """
    template_name = 'accounts/update_account.html'
    account = get_object_or_404(User, id=pk)
    form = UserUpdateForm(request.POST or None, request.FILES or None, instance=account)
    if form.is_valid():
        form.save()
        return redirect('account')
    context = {
        "form": form,
        "pk": pk
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def delete_account(request,pk):
    """
    This function deletes a user account with a specific primary key and redirects to the accounts list
    page.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user's request, such as the HTTP method used (GET, POST,
    etc.), the URL requested, any data submitted in the request, and more
    :param pk: pk stands for "primary key". In this context, it refers to the unique identifier of a
    specific user account in the database. The function is designed to delete the user account with the
    specified primary key (pk) and then redirect the user to the list of all remaining user accounts
    :return: a redirect to the 'accounts-list' URL after deleting the user account with the primary key
    (pk) specified in the request.
    """
    account = User.objects.filter(id=pk)
    account.delete()
    return redirect('account')

@login_required(login_url='/login')
def category(request):
    """
    This function retrieves a list of categories from the database, paginates them, and renders them in
    a template.
    
    :param request: The HTTP request object that contains information about the current request, such as
    the user's session and any submitted form data
    :return: The function `category(request)` returns an HTTP response with the rendered template
    `category/category_list.html` and a context dictionary containing a paginated list of `Category`
    objects ordered by their creation date, as well as a CSS style for the category state.
    """
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
def department(request):
    """
    This function retrieves a list of departments, paginates them, and renders them in a template.
    
    :param request: The HTTP request object that contains information about the current request,
    including the user's browser information, any submitted form data, and the requested URL
    :return: The function `department(request)` is returning an HTTP response with the rendered template
    `department/department_list.html` and a context dictionary containing a paginated list of
    `Department` objects, as well as a CSS style for the department state.
    """
    template_name = 'department/department_list.html'
    department = Department.objects.all().order_by('-created_at')
    paginator = Paginator(department, 10)
    page_number = request.GET.get('page')
    department = paginator.get_page(page_number)
    context = {
        "department": department,
        "department_state": "background-color: rgba(212, 210, 210, 1);  color: #fff;",
        # "breadcrumb": breadcrumb
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def add_department(request):
    template_name = 'department/add_department.html'
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('department')
    context = {
        "form": form,
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def update_department(request, pk):
    """
    This function updates a department object with the specified primary key (pk) based on the data
    provided in the request.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    headers, the body of the request, and any query parameters. In Django, the request object is an
    instance of the
    :param pk: "pk" stands for "primary key". In Django, the primary key is a unique identifier for each
    record in a database table. In this case, "pk" is being used as a parameter in a function that
    updates a department record in the database. The "pk" parameter is used to
    """
    template_name = 'department/update_department.html'
    department = get_object_or_404(Department, id=pk)
    form = DepartmentForm(request.POST or None, instance=department)
    if form.is_valid():
        form.save()
        return redirect('department')
    context = {
        "form": form,
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def delete_department(request, pk):
    """
    The function "delete_department" takes in a request and a primary key (pk) as parameters and likely
    deletes a department object from a database based on the pk.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user's request, such as the HTTP method used (GET, POST,
    etc.), any data submitted with the request, and the user's session information
    :param pk: "pk" stands for "primary key". In Django, the primary key is a unique identifier for each
    record in a database table. In this case, "pk" is the primary key of the department that needs to be
    deleted
    """
    department = Department.objects.filter(id=pk)
    department.delete()
    return redirect('department')

@login_required(login_url='/login')
def add_category(request):
    """
    The function "add_category" is likely a view function in a Django web application that handles
    requests to add a new category.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    URL requested, any data submitted in the request (such as form data), and any cookies or headers
    sent with the request
    """
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
    """
    This function is likely a view in a Django web application that updates a category object with the
    primary key (pk) specified in the URL.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (e.g. GET, POST), the
    headers sent with the request, and any data sent in the request body. In Django, the request object
    is automatically
    :param pk: pk stands for "primary key". In Django, primary keys are unique identifiers assigned to
    each record in a database table. In this case, the pk parameter is used to identify the specific
    category record that needs to be updated
    """
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
    """
    This function is likely a view in a Django web application that handles deleting a category object
    with a specific primary key (pk) from the database.
    
    :param request: The request object represents the current HTTP request that the user has made. It
    contains information about the user's request, such as the HTTP method used (GET, POST, etc.), any
    data submitted with the request, and the user's session information
    :param pk: "pk" stands for "primary key". In Django, the primary key is a unique identifier for each
    record in a database table. In this case, "pk" is the primary key of the category that the user
    wants to delete
    """
    category = Category.objects.filter(id=pk)
    category.delete()
    return redirect('category')

@login_required(login_url='/login')
def document(request):
    """
    The function "document" is not defined and therefore cannot be summarized.
    
    :param request: The `request` parameter in a Django view function represents an HTTP request that is
    sent by a client to the server. It contains information about the request, such as the URL, headers,
    and any data that was sent in the request body. The view function processes the request and returns
    an HTTP response
    """
    template_name = 'document/docu_list.html'
    document = Documents.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    # form = ForwardDocumentForm(request.POST or None, instance=forward) 
    paginator = Paginator(document, 10)
    page_number = request.GET.get('page')
    document = paginator.get_page(page_number)
    context = {
        "document": document,
        "document_state": "background-color: rgba(212, 210, 210, 1);  color: #fff;",
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def incoming_document(request):
    """
    The function "document" is not defined and therefore cannot be summarized.
    
    :param request: The `request` parameter in a Django view function represents an HTTP request that is
    sent by a client to the server. It contains information about the request, such as the URL, headers,
    and any data that was sent in the request body. The view function processes the request and returns
    an HTTP response
    """
    template_name = 'document/incoming_docu_list.html'

    document = Documents.objects.filter(receiver= request.user.department).order_by('-uploaded_at')
    # form = ForwardDocumentForm(request.POST or None, instance=forward) 
    paginator = Paginator(document, 10)
    page_number = request.GET.get('page')
    document = paginator.get_page(page_number)
    context = {
        "document": document,
        "document_state": "background-color: rgba(212, 210, 210, 1);  color: #fff;",
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def send_docu(request, pk):
    """
    The function "send_docu" takes in a request and a primary key as parameters.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    headers, the body of the request, and any query parameters. It is typically passed as the first
    parameter to a view
    :param pk: "pk" stands for "primary key". In Django, it is a unique identifier for a specific
    instance of a model. In this case, it is likely that the "send_docu" function is expecting a request
    object and a primary key value as parameters. The primary key value is used to
    """
    template_name = 'document/forward_doc.html'
    forward = get_object_or_404(Documents, id=pk)
    form = ForwardDocumentForm(request.POST or None, instance=forward)
    if form.is_valid():
        form.save()
        user = get_object_or_404(User, department=form.cleaned_data['receiver'])
        Notifications.objects.create(user = user, link=f"/document/view/{pk}", created_by=request.user,
                                     message = f"{request.user.first_name} {request.user.last_name} sent you a file",)
        return redirect('document')
    context = {
        "form": form,
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def receive_docu(request, pk):
    """
    The function "send_docu" takes in a request and a primary key as parameters.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    headers, the body of the request, and any query parameters. It is typically passed as the first
    parameter to a view
    :param pk: "pk" stands for "primary key". In Django, it is a unique identifier for a specific
    instance of a model. In this case, it is likely that the "send_docu" function is expecting a request
    object and a primary key value as parameters. The primary key value is used to
    """
    template_name = 'document/forward_doc.html'
    Documents.objects.filter(id=pk).update(is_received=True)
    user = get_object_or_404(Documents, id=pk)
    get_sender = Notifications.objects.filter(user=request.user).first()
    Notifications.objects.create(user = get_sender.created_by, link=f"/document/view/{pk}",
                                    message = f"{request.user.first_name} {request.user.last_name} received your file",)
    return redirect("/document/incoming")

@login_required(login_url='/login')
def add_docu(request):
    """
    The function "add_docu" is defined in Python and takes a request object as input.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by a
    client to a server. It contains information about the request, such as the HTTP method used (e.g.
    GET, POST), the URL requested, any query parameters, headers, and the body of the request (if
    """
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
    """
    This function retrieves a specific document object and renders it in a template for viewing.
    
    :param request: The HTTP request object that contains information about the current request, such as
    the user's browser information, the requested URL, and any data submitted in the request
    :param pk: pk stands for "primary key" and is used to identify a specific record in a database
    table. In this case, it is used to retrieve a specific document object from the Documents model
    :return: The view function `view_docu` returns an HTTP response rendered by the `render` function.
    The response contains the `view_docu.html` template rendered with the context dictionary `context`.
    """
    template_name = 'document/view_docu.html'
    document = Documents.objects.filter(id=pk)
    Notifications.objects.filter(link=f"/document/view/{pk}").update(is_read=True)
    context = {
        "document": document
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def update_docu(request, pk):
    """
    This function updates a document with a specific primary key.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    headers, the body of the request, and any query parameters. In Django, the request object is
    automatically created by the
    :param pk: "pk" stands for "primary key" and is a unique identifier for a specific object in a
    database table. In this case, it is likely referring to the primary key of a document that needs to
    be updated. The "request" parameter is an object that contains information about the current HTTP
    request
    """
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
    """
    This function takes a request and a primary key as input parameters and is likely used to delete a
    document from a database or file system.
    
    :param request: The request object represents the current HTTP request that the user has made. It
    contains information about the user's request, such as the HTTP method used (GET, POST, etc.), any
    data submitted with the request, and the user's session information
    :param pk: "pk" stands for "primary key". In Django, the primary key is a unique identifier for each
    record in a database table. In this case, the "delete_docu" function is likely deleting a document
    from a database table and the "pk" parameter is used to identify which document to
    """
    """
    This function takes a request and a primary key as input parameters and is likely used to delete a
    document from a database or file system.
    
    :param request: The request object represents the current HTTP request that the user has made. It
    contains information about the user's request, such as the HTTP method used (GET, POST, etc.), any
    data submitted with the request, and the user's session information
    :param pk: "pk" stands for "primary key". In Django, the primary key is a unique identifier for each
    record in a database table. In this case, the "delete_docu" function is likely deleting a document
    from a database table and the "pk" parameter is used to identify which document to
    """
    document = Documents.objects.get(id=pk)
    delete_history(
        user=f"{request.user.first_name}, {request.user.last_name}",
        history=f"The document titled {document.file_name} was deleted by {request.user.first_name}, {request.user.last_name} ",
        user_image = f"{request.user.profile_picture.url}"
    )
    document.delete()
    return redirect('document')

@login_required(login_url='/login')
def history(request):
    """
    The function "history" is defined in Python, but there is no code provided to determine its purpose
    or functionality.
    
    :param request: The request parameter in a Django view function represents an HTTP request that is
    sent by a client to the server. It contains information about the request, such as the URL, headers,
    and any data that was sent with the request. The view function processes the request and returns an
    HTTP response, which is
    """
    template_name = 'history/history_list.html'
    history = Notifications.objects.filter(user=request.user).order_by('-created_at')
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
    """
    The function "view_profile" is likely a view function in a Django web application that handles
    requests related to viewing a user's profile.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    URL requested, any data submitted in the request (such as form data), and any cookies or headers
    sent with the request
    """
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
    """
    The function is likely a view in a Django web application that handles updating a user's password.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (e.g. GET, POST), the URL
    requested, any query parameters, headers, and the request body. In this case, the `password
    """
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



def notification_count(request):
    count = Notifications.objects.filter(is_read=False, user=request.user).count()

    return JsonResponse(count, safe=False)