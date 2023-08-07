from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated

from users.models import User, Profession, Project
from users.serializers import UserSerializer, SearchSerializer, ProjectSerializer
from utils.baseapiviews import BaseAPIView, get_first_error_message_from_serializer_errors
from utils.baseauthentication import UserAuthentication
from utils.reusable_methods import split_full_name


class Signup(BaseAPIView):

    def post(self, request, *args, **kwargs):

        if not "email" in request.data:
            return self.send_bad_request_response(message="Email is required")
        if not "password" in request.data:
            return self.send_bad_request_response(message="Password is required")
        if not "full_name" in request.data:
            return self.send_bad_request_response(message="Fullname is required")
        if not "role" in request.data:
            return self.send_bad_request_response(message="Role is required")
        if User.objects.filter(email=request.data.get("email")).exists():
            return self.send_bad_request_response(message="Email already exists")
        if User.objects.filter(username=request.data.get("email").split("@")[0]).exists():
            return self.send_bad_request_response(message="Username already exists")

        fn, ln = split_full_name(request.data.get("full_name"))
        User.objects.create(
            username=request.data.get("email").split("@")[0],
            email=request.data.get("email"),
            password=make_password(request.data.get("password")),
            first_name=fn,
            last_name=ln,
            role=request.data.get("role"),
            name=request.data.get("full_name")
        )
        return self.send_success_response(
            message="Success",
        )


class Signin(BaseAPIView):
    serializer = UserSerializer

    def post(self, request, *args, **kwargs):
        if not "email" in request.data:
            return self.send_bad_request_response(message="Email is required")
        if not "password" in request.data:
            return self.send_bad_request_response(message="Password is required")

        user = User.objects.filter(email=request.data.get("email")).first()
        if user is None:
            return self.send_bad_request_response(message="Invalid user")
        if not user.check_password(request.data.get("password")):
            return self.send_bad_request_response(message="Invalid password")

        data = self.serializer(user).data
        return self.send_success_response("Success", data)


class SearchProfessionals(BaseAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [UserAuthentication]

    def get(self, request, *args, **kwargs):
        user_ids = None
        data = dict()
        profession = request.query_params.get("profession")
        if profession:
            user_ids = list(Profession.objects.filter(profession_name__icontains=profession).values_list("user", flat=True))
        else:
            user_ids = list(User.objects.filter(role=1).values_list("id", flat=True))
        if user_ids:
            users = User.objects.filter(id__in=user_ids)
            data = SearchSerializer(users, many=True).data
        return self.send_success_response("Succss", data)


class UpdateProfessionProfile(BaseAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [UserAuthentication]
    serializer = UserSerializer


    def patch(self, request, *args, **kwargs):
        userializer = self.serializer(request.user, request.data, partial=True)
        if userializer.is_valid():
            userializer.save()
            return self.send_success_response("Success", self.serializer(request.user).data)
        return self.send_bad_request_response(get_first_error_message_from_serializer_errors(userializer.errors))


class ProjectView(BaseAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [UserAuthentication]
    serializer = ProjectSerializer

    def post(self, request, *args, **kwargs):

        project_serializer = ProjectSerializer(data=request.data, context={"request": request})
        if project_serializer.is_valid():
            project_serializer.save()
            return self.send_success_response("Success")
        return self.send_bad_request_response(get_first_error_message_from_serializer_errors(project_serializer.errors))

    def get(self, request, *args, **kwargs):
        instances = Project.objects.filter(user=request.user)
        return self.send_success_response("Success", self.serializer(instances, many=True).data)
