# Django imports
from django.urls import path
# Import views from current directory
from . import views as v


# Set application namespace for URL patterns
app_name = "main"

# URL patterns for main app
urlpatterns = [
    # Homepage URL pattern
    path("", v.home, name="home"),
    # Logout URL pattern
    path("logout/", v.logout, name="logout"),
]
