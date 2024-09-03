from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, TemplateView

from .forms import CustomerSignUpForm, CompanyRegistrationForm
from .models import Company, User


def register(request):
    return render(request, "users/register.html")


# class CustomerSignUpView(CreateView):
#     model = User
#     form_class = CustomerSignUpForm
#     template_name = "users/register_customer.html"

#     def get_context_data(self, **kwargs):
#         kwargs["user_type"] = "customer"
#         return super().get_context_data(**kwargs)

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect("/")


# class CompanySignUpView(CreateView):
#     model = User
#     form_class = CompanySignUpForm
#     template_name = "users/register_company.html"

#     def get_context_data(self, **kwargs):
#         kwargs["user_type"] = "company"
#         return super().get_context_data(**kwargs)

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect("/")


def LoginUserView(request):
    pass


def register_company(request):
    if request.method == "POST":
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_company = True
            user.set_password(form.cleaned_data["password"])
            user.save()
            Company.objects.create(
                user=user,
                username=user.username,  # Or some other field value
                email=user.email,
                field_of_work=form.cleaned_data["field_of_work"],
            )
            return redirect("main:home")
    else:
        form = CompanyRegistrationForm()

    return render(request, "register_company.html", {"form": form})
