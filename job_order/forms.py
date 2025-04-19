from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['employee_id', 'full_name', 'email']



def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Ensure the password is hashed before saving
            user.set_password(form.cleaned_data['password1'])  # Hash the password
            user.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')  # Redirect to login after successful sign-up
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'job_order/signup.html', {'form': form})
