from django.shortcuts import render, redirect
from .models import User

# Create your views here.

def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not all([name, email, username, password, confirm_password]):
            return render(request, "MK_sample login_signup.html", {"error": "All fields are required"})
        
        if User.objects.filter(email=email).exists():
            return render(request, "MK_sample login_signup.html", {"error": "Email already in use"})
        
        if User.objects.filter(username=username).exists():
            return render(request, "MK_sample login_signup.html", {"error": "Username already in use"})
        
        if password == confirm_password:
            user = User(name=name, email=email, username=username)
            user.SetPassword(password)
            user.save()
            
            return redirect("login")
        else:
            return render(request, "MK_sample login_signup.html", {"error": "Passwords do not match"})

    return render(request, "MK_sample login_signup.html")

def login(request):
    if request.method == "POST":
        login_input = request.POST.get("email")
        password = request.POST.get("password")

        if not all([login_input, password]):
            return render(request, "MK_sample login_signup.html", {"error": "All fields are required"})

        user = User.objects.filter(username=login_input).first() or User.objects.filter(email=login_input).first()

        if user and user.CheckPassword(password):
            request.session["user_id"] = user.id
            return redirect("how_it_works")  ##redirect to the main app once login is successful here is where the login connects to the main app
        else:
            return render(request, "MK_sample login_signup.html", {"error": "Invalid credentials"})

    return render(request, "MK_sample login_signup.html")

def logout(request):
    request.session.flush()  # Clears all session data
    return redirect("login") # Redirect to login page after logout