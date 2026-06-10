from django.shortcuts import render, redirect
from .models import User
from .forms import SignupForm

# Create your views here.

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
            return redirect("login")
    return render(request, "login_signup.html", {"signup_form": form})

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