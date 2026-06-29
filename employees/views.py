from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login, logout
from .models import Employee
from .forms import EmployeeForm

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('employee_list')
    
    form  = AuthenticationForm(request, data = request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('employee_list')
    return render(request, 'employees/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def employee_list(request):
    if request.user.is_authenticated:
        query = request.GET.get('q')
        if query:
            employees = Employee.objects.filter(
                Q(name__icontains=query) | Q(department__icontains=query)
            )
        else:
            employees = Employee.objects.all()
        return render(request, 'employees/employee_list.html', {'employees': employees})
    return redirect('login')

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

@login_required
def employee_create(request):
    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('employee_list')
    return render(request, 'employees/employee_form.html', {'form': form})

@login_required
def employee_update(request,pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, instance=employee)
    if form.is_valid():
        form.save()
        return redirect('employee_list')
    
    return render(request, 'employees/employee_form.html', {'form': form})

@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == "POST":
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee':employee})

