from .serializers import (
    LoginSerializer, RegisterSerializer, ActivationSerializer, CheckEmailSerializer, ChangePasswordSerializer,
    ResetPasswordCompleteSerializer)
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, smart_bytes
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ActivationView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ActivationSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs.get(self.lookup_field)
        id_ = smart_str(urlsafe_base64_decode(uuid))
        return User.objects.get(id=id_)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ResetPasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CheckEmailSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_email = serializer.validated_data.get('email')
        user = User.objects.get(email=user_email)

        uuid = urlsafe_base64_encode(smart_bytes(user.id))

        link = request.build_absolute_uri(reverse_lazy("accounts:reset_password_complete", kwargs={"uuid": uuid}))

        message = f'You can reset password by clicking the link below: \n {link}'

        send_mail(
            "Jobify | Reset Password",
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )

        return Response(serializer.data, status=201)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    lookup_field = "uuid"


    def put(self, *args, **kwargs):
        if self.get_object() == self.request.user:
            user = self.get_object()
            serializer = self.serializer_class(data=self.request.data, context={"request": self.request})
            serializer.is_valid(raise_exception=True)

            user.set_password(serializer.validated_data.get('password'))

            user.save()

            token_data = {"email": user.email}

            token = RefreshToken.for_user(user)
            token_data["token"] = {"refresh": str(token), "access": str(token.access_token)}
        else:
            raise ValueError({"error": "Wrong link"})

        return Response({**token_data})


class ResetPasswordCompleteView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordCompleteSerializer
    lookup_field = 'uuid'

    def get_object(self):
        uuid = self.kwargs.get(self.lookup_field)
        id_ = smart_str(urlsafe_base64_decode(uuid))
        return User.objects.get(id=id_)

    def put(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data.get('password'))
        user.save()

        token_data = {'email': user.email}

        token = RefreshToken.for_user(user)

        token_data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}

        return Response({**token_data})
