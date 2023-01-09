from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainSlidingView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from .serializers import TokenObtainSerializer, UserRegistrationSerializer


User = get_user_model()


class TokenObtainView(TokenObtainSlidingView):
    "View для получения JWT"
    serializer_class = TokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.POST)
        if serializer.is_valid():
            if 'error' in serializer.validated_data:
                return Response(
                    serializer.validated_data,
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(APIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        user = User.objects.filter(**serializer.data).last()
        if user:
            code = default_token_generator.make_token(user)
            send_mail(
                'Код для получения токена',
                f'Код для получения JWT токена: {code}',
                'yamdb@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
