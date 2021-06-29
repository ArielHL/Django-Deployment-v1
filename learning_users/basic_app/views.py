from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("Logged successfully")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered=False

    if request.method == 'POST':
        # take the info from the form
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST) 
        # check if the form is valid
        if user_form.is_valid() and profile_form.is_valid():

            # saving the form into the database
            user=user_form.save()     
            # hashing the password
            user.set_password(user.password)
            #save the hashed password into the database
            user.save()

            profile=profile_form.save(commit=False)
            # profile==profile_form that is == to UserProfileInfoForm that is connected with UserProfileInfo model 
            # this models contain three objets, the original User built in fields under user objetct and the additional fields, this 
            # that user field is connected with the User Form
            profile.user = user   #this connect the form object UserProfileInfoForm with the form object userform que es user

            #check if there is actually a picture in the form before save it
            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()

            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()
    return render(request,'basic_app/registration.html',
                                                        {'user_form':user_form,
                                                        'profile_form':profile_form,
                                                        'registered':registered})


def user_login(request):

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)   # this return a Boolean True or False

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("someone tried to login and failed!")    
            print("Username:{} and pasword {}".format(username,password))
            return HttpResponse("Invalid login Details Supplied!")
    
    else:
        return render(request,'basic_app/login.html',{})
