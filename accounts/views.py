from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser as User


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role')  # 'vendor' or 'customer'

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password, email=email)
        if role == 'vendor':
            user.is_vendor = True
        elif role == 'customer':
            user.is_customer = True
        user.save()

        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')
    
    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Role-based redirect
            if user.is_vendor:
                return redirect('vendor_dashboard')
            elif user.is_customer:
                return redirect('customer_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})


@login_required(login_url='login')
def vendor_dashboard_view(request):
    if request.user.is_vendor:
        return render(request, 'accounts/vendor_dashboard.html', {'user': request.user})
    else:
        messages.error(request, "You are not authorized to access the vendor dashboard.")
        return redirect('dashboard')


@login_required(login_url='login')
def customer_dashboard_view(request):
    if request.user.is_customer:
        return render(request, 'accounts/customer_dashboard.html', {'user': request.user})
    else:
        messages.error(request, "You are not authorized to access the customer dashboard.")
        return redirect('dashboard')
