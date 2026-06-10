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
            return render(request, "login_signup.html", {"error": "All fields are required"})
        
        if User.objects.filter(email=email).exists():
            return render(request, "login_signup.html", {"error": "Email already in use"})
        
        if User.objects.filter(username=username).exists():
            return render(request, "login_signup.html", {"error": "Username already in use"})
        
        if password == confirm_password:
            user = User(name=name, email=email, username=username)
            user.set_password(password)
            user.save()
            
            return redirect("login")
        else:
            return render(request, "login_signup.html", {"error": "Passwords do not match"})

    return render(request, "login_signup.html")

def login(request):
    if request.method == "POST":
        login_input = request.POST.get("email")
        password = request.POST.get("password")

        if not all([login_input, password]):
            return render(request, "login_signup.html", {"error": "All fields are required"})

        user = User.objects.filter(username=login_input).first() or User.objects.filter(email=login_input).first()

        if user and user.check_password(password):
            request.session["user_id"] = user.id
            return redirect("how_it_works")
        else:
            return render(request, "login_signup.html", {"error": "Invalid credentials"})

    return render(request, "login_signup.html")

def logout(request):
    request.session.flush()  # Clears all session data
    return redirect("login") # Redirect to login page after logout