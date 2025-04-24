from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User, Profile
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import (
    RegistrationSerializers,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    DummySerializer,
    ResendUserVerificationSerializers,
    PasswordRestViewSerializer,
    PasswordRestViewLinkSerializer,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

# from mail_templated import send_mail
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import EmailThread
import jwt
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, DecodeError
from django.contrib.auth import get_user_model


User = get_user_model()


class RegistrationView(GenericAPIView):
    serializer_class = RegistrationSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        email = serializer.validated_data["email"]
        data = {"email": email}

        user_obj = get_object_or_404(User, email=email)
        token = self.get_tokens_for_user(user_obj)

        email_obj = EmailMessage(
            "email/activation.tpl",
            {"token": token},
            "admin@admin.com",
            to=[email],
        )
        EmailThread(email_obj).start()

        return Response(data, status=status.HTTP_201_CREATED)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": user.pk, "email": user.email}
        )


class CustoumDiscordeCustom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except ObjectDoesNotExist:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"success": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )


class ProfileApiView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class TestEmailSend(GenericAPIView):
    serializer_class = DummySerializer

    def get(self, request, *args, **kwargs):
        # send_mail(
        #     "Subject here",
        #     "Here is the message.",
        #     "from@example.com",
        #     ["to@example.com"],
        #     fail_silently=False,
        #     )
        # send_mail('email/hello.tpl', {'user': "reza"}, "admin@admin.com", ["reza@reza.com"])
        self.mail = "reza@reza.com"
        user_obj = get_object_or_404(User, email=self.mail)
        token = self.get_tokens_for_user(user_obj)

        email_obj = EmailMessage(
            "email/hello.tpl",
            {"user": {"name": "Reza"}, "token": token},
            "admin@admin.com",
            to=[self.mail],
        )

        EmailThread(email_obj).start()
        return Response(
            {"detail": "Email was sent successfully."},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class UserVerification(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = payload.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"detail": "Token has expired."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except DecodeError:
            return Response(
                {"detail": "Invalid token."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_obj = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if user_obj.is_verified:
            return Response(
                {"detail": "You're already verified!"},
                status=status.HTTP_200_OK,
            )

        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"detail": "You're verified!"}, status=status.HTTP_200_OK
        )


class ResendUserVerification(GenericAPIView):
    serializer_class = ResendUserVerificationSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)

        email_obj = EmailMessage(
            "email/activation.tpl",
            {"token": token, "user": user_obj},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()

        return Response(
            {"detail": "Activation email sent."},
            status=status.HTTP_201_CREATED,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class PasswordRestView(GenericAPIView):
    serializer_class = PasswordRestViewSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)

        email_obj = EmailMessage(
            "email/password_rest.tpl",
            {"token": token},
            "admin@admin.com",
            to=[email],
        )
        EmailThread(email_obj).start()

        return Response({"email": email}, status=status.HTTP_200_OK)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class PasswordRestLink(GenericAPIView):
    serializer_class = PasswordRestViewLinkSerializer

    def get(self, request, token, *args, **kwargs):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = payload.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"detail": "Token has expired."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except DecodeError:
            return Response(
                {"detail": "Invalid token."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_obj = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # اینجاست که برای reset فرم به فرانت می‌تونی پیام بدی که مثلا "token is valid"
        return Response(
            {"detail": "Token is valid."}, status=status.HTTP_200_OK
        )

    def post(self, request, token, *args, **kwargs):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = payload.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"detail": "Token has expired."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except DecodeError:
            return Response(
                {"detail": "Invalid token."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_obj = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(
            data=request.data, context={"user": user_obj}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "Password has been reset successfully."},
            status=status.HTTP_200_OK,
        )
