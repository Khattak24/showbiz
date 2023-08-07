from django.urls import path
from users.views import Signup, Signin, SearchProfessionals, UpdateProfessionProfile, ProjectView

urlpatterns = [
    path("sign-up/", Signup.as_view()),
    path("sign-in/", Signin.as_view()),
    path("update-profile/", UpdateProfessionProfile.as_view()),
    path("search-professionals", SearchProfessionals.as_view()),
    path("project", ProjectView.as_view())
]