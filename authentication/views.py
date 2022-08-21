from .models import Profile
from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from utilities.permissions import ReadOnly
from .serializers import (
    RegisterSerializer,
    SetNewPasswordSerializer,
    ResetPasswordEmailRequestSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    LogoutSerializer,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from .renderers import UserRenderer
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from .utils import Util
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
import os


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        print(user, "7" * 80)
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        print(token, "8" * 80)
        relativeLink = reverse("authentication:email-verify")
        absurl = current_site + relativeLink + "?token=" + str(token)
        email_body = (
            "Hi "
            + user.username
            + " Use the link below to verify your email \n"
            + absurl
        )
        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Verify your email",
        }

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="Description",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get("token")
        print(settings.SECRET_KEY)
        print(token)
        try:  # TODO
            payload = jwt.decode(
                jwt=str(token), key=str(settings.SECRET_KEY), algorithms=["HS256"]
            )
            user = User.objects.get(id=payload["user_id"])

            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()
                Profile.objects.create(user=user)

            data = {
                "refresh": user.tokens()["refresh"],
                "access": user.tokens()["access"],
            }
            return Response({"data": data}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.user.email

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse(
                "authentication:password-reset-confirm",
                kwargs={"uidb64": uidb64, "token": token},
            )
            absurl = "http://" + current_site + relativeLink
            email_body = "Hello, \n Use link below to reset your password  \n" + absurl
            data = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "Reset your passsword",
            }
            # Util.send_email(data)
            # print(data)
            return Response(
                {"success": "We have sent you a link to reset your password"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Email does not exists"}, status=status.HTTP_400_BAD_REQUEST
            )


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"error": "Token is not valid, please request a new one"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            return Response(
                {
                    "success": True,
                    "message": "Credentials Valid",
                    "uidb64": uidb64,
                    "token": token,
                },
                status=status.HTTP_200_OK,
            )
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response(
                    {"error": "Token is not valid, please request a new one"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [
        AllowAny,
    ]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": True, "message": "Password reset success"},
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ForgetPasswordAPIView(generics.GenericAPIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        email = request.POST["email"]

        if User.objects.filter(email=email).exists():
            # sending activation email
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            # using PasswordResetTokenGenerator to create token
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse(
                "authentication:password-reset-confirm",
                kwargs={"uidb64": uidb64, "token": token},
            )
            absurl = "http://" + current_site + relativeLink
            email_body = "Hello, \n Use link below to change your password  \n" + absurl
            data = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "Reset your passsword",
            }
            # print(data)
            return Response(
                {"success": "We have sent you a link to reset your password"},
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                {"error": "Email does not exists"}, status=status.HTTP_400_BAD_REQUEST
            )
