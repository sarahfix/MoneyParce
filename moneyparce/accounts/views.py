from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout

def reset_password(request):
    template_data = {}
    template_data['title'] = 'Reset Password'

    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        try:
            # Fetch user by username
            user = User.objects.get(username=username)
            user.set_password(new_password)  # Set new password
            user.save()

            # Optionally, log out the user for security purposes
            auth_logout(request)

            template_data['success'] = 'Password has been updated successfully.'
            return redirect('accounts.login')  # Redirect to login after reset

        except User.DoesNotExist:
            template_data['error'] = 'The username provided does not exist.'
            return render(request, 'accounts/reset_password.html', {'template_data': template_data})

    # Ensure that we return a response for GET requests
    return render(request, 'accounts/reset_password.html', {'template_data': template_data})



@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')


def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = UserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                          {'template_data': template_data})

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()  # Deletes the authenticated user
        return redirect("home.index")  # Redirect to home after deletion

    return render(request, "accounts/delete_account.html")  # Show confirmation page

# Create your views here.
