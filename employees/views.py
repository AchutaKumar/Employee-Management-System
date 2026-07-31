from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Avg, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date, timedelta
from .models import Employee
from .forms import EmployeeForm, CustomLoginForm, CustomUserCreationForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('employee_list')
    
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created successfully! Welcome, {user.username}.")
            return redirect('employee_list')
        else:
            messages.error(request, "Registration failed. Please fix the errors below.")
            
    return render(request, 'employees/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('employee_list')
    
    form = CustomLoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('employee_list')
    return render(request, 'employees/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')

@login_required
def employee_list(request):
    # Auto-claim unassigned legacy employees for current user if user has none
    if not Employee.objects.filter(user=request.user).exists() and Employee.objects.filter(user__isnull=True).exists():
        Employee.objects.filter(user__isnull=True).update(user=request.user)

    # Handle Reset Session State request
    if request.GET.get('reset') == 'true':
        request.session.pop('employee_filters', None)
        messages.info(request, "Search and filter session state cleared.")
        return redirect('employee_list')

    # Session State Management: read from GET or restore from user session
    saved_filters = request.session.get('employee_filters', {})
    
    if any(k in request.GET for k in ('q', 'department', 'status')):
        query = request.GET.get('q', '').strip()
        selected_dept = request.GET.get('department', '').strip()
        selected_status = request.GET.get('status', '').strip()
        request.session['employee_filters'] = {
            'q': query,
            'department': selected_dept,
            'status': selected_status,
        }
    else:
        query = saved_filters.get('q', '')
        selected_dept = saved_filters.get('department', '')
        selected_status = saved_filters.get('status', '')

    # Filter employees specifically for the authenticated user
    employees = Employee.objects.filter(user=request.user).order_by('-id')

    if query:
        employees = employees.filter(
            Q(name__icontains=query) | 
            Q(department__icontains=query) | 
            Q(role__icontains=query) | 
            Q(email__icontains=query)
        )

    if selected_dept and selected_dept != 'All Departments':
        employees = employees.filter(department=selected_dept)

    if selected_status and selected_status != 'All Statuses':
        employees = employees.filter(status=selected_status)

    total_employees = Employee.objects.filter(user=request.user).count()
    departments_list = Employee.objects.filter(user=request.user).values_list('department', flat=True).distinct()
    
    # New hires in last 365 days or recent 12 for this specific user
    one_year_ago = date.today() - timedelta(days=365)
    new_hires_count = Employee.objects.filter(user=request.user, joining_date__gte=one_year_ago).count()
    if new_hires_count == 0:
        new_hires_count = min(total_employees, 12)

    # Django Pagination (5 items per page)
    per_page = 5
    paginator = Paginator(employees, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    has_active_session_filter = bool(query or (selected_dept and selected_dept != 'All Departments') or (selected_status and selected_status != 'All Statuses'))

    context = {
        'page_obj': page_obj,
        'employees': page_obj.object_list,
        'paginator': paginator,
        'query': query,
        'selected_dept': selected_dept,
        'selected_status': selected_status,
        'departments_list': departments_list,
        'total_employees': total_employees,
        'new_hires_count': new_hires_count,
        'results_count': employees.count(),
        'has_active_session_filter': has_active_session_filter,
    }
    return render(request, 'employees/employee_list.html', context)

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk, user=request.user)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

@login_required
def employee_create(request):
    form = EmployeeForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            employee = form.save(commit=False)
            employee.user = request.user
            employee.save()
            messages.success(request, f"Employee '{employee.name}' added successfully!")
            return redirect('employee_list')
        else:
            messages.error(request, "Please correct the errors in the form below.")
    return render(request, 'employees/employee_form.html', {'form': form})

@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk, user=request.user)
    form = EmployeeForm(request.POST or None, instance=employee)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f"Employee '{employee.name}' updated successfully!")
            return redirect('employee_list')
        else:
            messages.error(request, "Please correct the errors in the form below.")
    return render(request, 'employees/employee_form.html', {'form': form, 'employee': employee})

@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk, user=request.user)
    if request.method == "POST":
        emp_name = employee.name
        employee.delete()
        messages.success(request, f"Employee '{emp_name}' deleted successfully!")
        return redirect('employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})

