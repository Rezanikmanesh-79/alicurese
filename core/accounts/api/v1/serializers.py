from rest_framework import serializers, serializers
from accounts.models import User, Profile
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationSerializers(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError(
                {"detail": "password doesn't match"}
            )
        try:
            attrs.pop("password1")
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        return attrs

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            ##### imported ######
            if not user.is_verified:
                msg = _("User is not verified.")
                raise serializers.ValidationError(msg, code="not_verified")

        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validate_data = super().validate(attrs)
        validate_data["email"] = self.user.email
        validate_data["user_id"] = self.user.id
        return validate_data


class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    new_password1 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user = self.context.get("user")

        # چک ایمیل
        if attrs.get("email") != user.email:
            raise serializers.ValidationError(
                {"email": "Email does not match logged-in user."}
            )

        # چک پسورد قدیمی
        if not user.check_password(attrs.get("old_password")):
            raise serializers.ValidationError(
                {"old_password": "Old password is incorrect."}
            )

        # چک مطابقت پسورد جدید
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError(
                {"detail": "Passwords don't match."}
            )

        # چک قوی بودن پسورد جدید
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": e.messages})

        return attrs

    def save(self, **kwargs):
        user = self.context.get("user")
        user.set_password(self.validated_data.get("new_password"))
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.CharField(source="user.email")

    class Meta:
        model = Profile
        fields = ["id", "email", "name", "last_name", "image"]
        read_only_fields = ["email"]


class DummySerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResendUserVerificationSerializers(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_ob = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "user dose not exist"}
            )
        if user_ob.is_verified:
            raise serializers.ValidationError(
                {"detail": "user already verified"}
            )
        attrs["user"] = user_ob
        return super().validate(attrs)


class PasswordRestViewSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_ob = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "User does not exist"}
            )
        attrs["user"] = user_ob
        return attrs


class PasswordRestViewLinkSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["password", "password1"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError(
                {"detail": "Passwords do not match."}
            )

        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        attrs.pop("password1")
        return attrs

    def create(self, validated_data):
        user = self.context["user"]
        user.set_password(validated_data["password"])
        user.save()
        return user
