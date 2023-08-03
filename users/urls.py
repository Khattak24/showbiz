from django.urls import path
from users.views import Signup, Signin, SearchProfessionals, UpdateProfessionProfile

urlpatterns = [
    path("sign-up/", Signup.as_view()),
    path("sign-in/", Signin.as_view()),
    path("update-profile/", UpdateProfessionProfile.as_view()),
    path("search-professionals", SearchProfessionals.as_view())
]