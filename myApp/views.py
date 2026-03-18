import pyrebase


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib.auth.models import User

from .models import QuoteRequest







# -----------------------------
# Firebase configuration
# -----------------------------
config = {
    "apiKey": "AIzaSyAdUOhxMN4zyQoqd9RZhefOFctAOyjqXRM",
    "authDomain": "job-application-tracker-bfcdf.firebaseapp.com",
    "projectId": "job-application-tracker-bfcdf",
    "storageBucket": "job-application-tracker-bfcdf.appspot.com",
    "messagingSenderId": "216938211667",
    "appId": "1:216938211667:web:472cd9339b8d8064d999a6",
    "measurementId": "G-SFGJX0YD0X",
    "databaseURL": "https://job-application-tracker-bfcdf-default-rtdb.firebaseio.com"
}

# -----------------------------
# Initialize Firebase (Python)
# -----------------------------
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# -----------------------------
# Django Views
# -----------------------------

def home(request):
    return render(request, "myApp/home.html")  # note the app folder prefix

def about(request):
    return render(request, "myApp/about.html")

def services(request):

    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        service = request.POST.get("service")
        needs = request.POST.get("needs")

        QuoteRequest.objects.create(
            fullname=fullname,
            email=email,
            phone=phone,
            service=service,
            needs=needs
        )

        messages.success(request, "Your quote request has been sent successfully!")

    return render(request, "myApp/services.html")

def careers(request):
    return render(request, "myApp/careers.html")

def contact(request):
    return render(request, "myApp/contact.html")


def signin(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "myApp/signin.html")


def signup(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")  # will be the username
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # 1️⃣ Password match check
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "myApp/signup.html")

        # 2️⃣ Check if email already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already in use")
            return render(request, "myApp/signup.html")

        try:
            # 3️⃣ Create user with email as username
            user = User.objects.create_user(
                username=email,  # now email is the username
                email=email,
                password=password,
                first_name=firstname,
                last_name=lastname
            )
            user.is_active = True
            user.save()

            print("User created:", user.username, "ID:", user.id)
            messages.success(request, "Account created successfully! Please sign in.")
            return redirect('signin')

        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return render(request, "myApp/signup.html")

    return render(request, "myApp/signup.html")

    
def hrsignin(request):
    return render(request, "myApp/hrsignin.html")

def profile(request):
    return render(request, "myApp/profile.html")

def notifications(request):
    return render(request, "myApp/notifications.html")

def inbox(request):
    return render(request, "myApp/inbox.html")

def settings(request):
    return render(request, "myApp/settings.html")

def feedback(request):
    return render(request, "myApp/feedback.html")

def help(request):
    return render(request, "myApp/help.html")



def apply(request):
    job_title = None

    if request.method == "POST":
        job_title = request.POST.get("job_title")

    return render(request, "myApp/apply.html", {"job_title": job_title})