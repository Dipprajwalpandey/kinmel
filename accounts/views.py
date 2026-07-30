from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .models import Profile


# ==================== SIGNUP VIEW ====================
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Registration successful! Welcome to our store.")
            return redirect('StoreHome')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


# ==================== PROFILE VIEW (READ-ONLY) ====================
@login_required
def profile_view(request):
    # Safely gets the profile, or creates it if missing
    profile, created = Profile.objects.get_or_create(user=request.user)

    context = {
        'profile': profile,
        'user': request.user
    }
    return render(request, 'accounts/profile.html', context)


# ==================== PROFILE EDIT VIEW ====================
@login_required
def edit_profile_view(request):
    # Safely gets the profile, or creates it if missing
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()

        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.address = request.POST.get('address', profile.address)
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        profile.save()

        messages.success(request, "Your profile details updated successfully!")
        return redirect('profile_view')

    context = {
        'profile': profile,
        'user': request.user
    }
    return render(request, 'accounts/edit_profile.html', context)