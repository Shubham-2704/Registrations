from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from myproject.settings import EMAIL_HOST_USER
from .models import UserProfile
from django.core.files.storage import default_storage
import re
from django.views.decorators.cache import never_cache



# Create your views here.

def index (request):
    return render (request ,'index.html')

@never_cache
def loginpage (request):
    if request.method == "POST":
        uname = request.POST.get ("username")
        pass1 = request.POST.get ("password")
        user = authenticate (request, username = uname, password = pass1)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the view name, not template file
        else:
            messages.error(request, "Username or Password is incorrect.")
    return render (request ,'login.html')

@never_cache
def signuppage (request):
    if request.method == "POST":
        uname = request.POST.get ("username")
        lname = request.POST.get ("lastname")
        fname = request.POST.get ("firstname")
        email = request.POST.get ("email")
        pass1 = request.POST.get ("password1")
        pass2 = request.POST.get ("password2")

        if pass1 != pass2:
            messages.error (request , "Your Password and Confirm Password do not match.")
            return redirect ('signup')
        
        if User.objects.filter (username = uname).exists():
            messages.error (request, "Username already taken. Please choose another one.")
            return redirect ('signup')
        
        if User.objects.filter (email = email).exists():
           messages.error (request, "Email is already registered. Try logging in instead.") 
           return redirect ('signup')
        
        my_user = User.objects.create_user (uname, email, pass1)
        my_user.first_name = fname
        my_user.last_name = lname
        my_user.save()
        UserProfile.objects.create(user=my_user)
        messages.success (request, "Your account has been successfully created. You can now log in.")
        return redirect ('login')

    return render (request ,'signup.html')

def forgotpassword (request):
    if request.method == "POST":
        email = request.POST.get ("email")
        print(email)

        if User.objects.filter (email = email).exists():
            user = User.objects.get (email = email)
            print("User Exists")

            send_mail ("Reset Your Password : ", f"Hey User : {user}! To Reset Password, Click on the Given Link \n http://127.0.0.1:8000/resetpassword/{user}/", EMAIL_HOST_USER, [email], fail_silently=True)
            messages.success (request, f"Hey User : {user}! A password reset link has been sent to your email. Please check your inbox.")
        
        else:
            messages.error(request, "No account found with this email address.")

        return render (request ,'forgotpassword.html')
    return render (request ,'forgotpassword.html')

def resetpassword (request, user):
    userid = User.objects.get (username = user)
    print(userid)
    if request.method == "POST":
        pass1 = request.POST.get ("newpassword")
        pass2 = request.POST.get ("confirmpassword")
        print(pass1, pass2)

        if pass1 != pass2:
            messages.error (request , "Your Password and Confirm Password do not match.")


        if pass1 == pass2:
            userid.set_password(pass1)
            userid.save()
            messages.success (request, "Your Password has been successfully Changed. You can now log in.")
            # return redirect ('login')

    return render (request ,'resetpassword.html')

@never_cache
def logoutpage (request):
    logout (request)
    return redirect ('index')

@never_cache
@login_required(login_url='login')
def profilepage (request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        dob = request.POST.get("dob")
        if dob:  # Only update if a value is provided
            user_profile.dob = dob

    if request.method == "POST":
        mobile_number = request.POST.get("mobile_number")

        # Validate Mobile Number (10 digits only)
        if not re.fullmatch(r"^\d{10}$", mobile_number):
            messages.error(request, "Invalid Mobile Number! Enter a 10-digit number only.")
            return redirect("profile")
        
        user_profile.gender = request.POST.get("gender")
        user_profile.mobile_number = request.POST.get("mobile_number")
        user_profile.address = request.POST.get("address")

        if 'profile_photo' in request.FILES:
            print("File detected:", request.FILES['profile_photo'])  # Debugging print
            if user_profile.profile_photo:
                print("Deleting old photo:", user_profile.profile_photo.path)  # Debugging print
                default_storage.delete(user_profile.profile_photo.path)  # Delete old photo
            
            user_profile.profile_photo = request.FILES['profile_photo']
        else:
            print("No file detected in request.")  # Debugging print



        user_profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    return render (request, 'profile.html', {"user_profile": user_profile})




