from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from users.forms import LoginForm


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username = username, password = password)

            if user:
                login(request, user)
                next_url = request.POST.get("next")
                if next_url:
                    return redirect(next_url)

                return redirect("/accounts/")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)

    return redirect("/login/")
