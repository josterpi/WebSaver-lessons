from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User
from .forms import SignupForm


def signup(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                username=form.cleaned_data["username"],
            )
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("login")
    return render(request, "login_signup.html", {"signup_form": form})


def login(request):
    if request.method == "POST":
        login_input = request.POST.get("email")
        password = request.POST.get("password")

        if not all([login_input, password]):
            return render(request, "login_signup.html", {"error": "All fields are required"})

        user = authenticate(request, username=login_input, password=password)
        if user is None:
            try:
                user_obj = User.objects.get(email=login_input)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user is not None:
            auth_login(request, user)
            return redirect("how_it_works")

        return render(request, "login_signup.html", {"error": "Invalid credentials"})

    return render(request, "login_signup.html")


def logout(request):
    auth_logout(request)
    return redirect("login")
