from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)

        if user:
            login(request, user)
            next_url = request.POST.get("next")
            if next_url:
                return redirect(next_url)

            return redirect("/accounts/accounts/")

    return render(request, "login.html")

def logout_view(request):
    logout(request)

    return redirect("/users/login/")
