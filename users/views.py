from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Admins, Space
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        name=request.POST.get('username')
        num=request.POST.get('size')
        email=request.POST.get('email')
        if form.is_valid():
            form.save()

            Space(name=name,num=num,email=email).save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)




def adminDash(request):
    usersData = Space.objects.all()
    return render(request,"users/admindash.html",{'userData':usersData})


def adminlogin(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        password=request.POST.get('password')
        usersData = Admins.objects.all()
        for i in usersData:
            if i.name==name and i.passwod==password:
                return redirect('admindash')
            else:
                pass
    return render(request,"users/adminlogin.html")





def StatusUpdate(request,pk):
    #https://www.google.com/settings/security/lesssecureapps
    user_instance = Space.objects.filter(id = pk).update(status = "Approved")
   
    return redirect('admindash')








    






