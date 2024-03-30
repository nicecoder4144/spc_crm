from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView 
from rest_framework.generics import GenericAPIView # new
from rest_framework.response import Response 
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, \
    HTTP_204_NO_CONTENT # new

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Field, Role, Worker, Student
from .serializers import FieldSerializer, RoleSerializer, WorkerSerializer, StudentSerializer,\
    FieldAPISerializer, WorkerAPISerializer, RoleAPISerializer, StudentAPISerializer,\
    UserRegistrationSerializer, UserLoginSerializer, LogoutSerializer, UserChangePasswordSerializer, \
        SendPasswordResetEmailSerializer, UserPasswordResetSerializer # new
from .renderers import UserRenderer

# Create your views here.

""" CRUD API """
class FieldViewset(ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    lookup_field = 'slug'

class RoleViewset(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

class WorkerViewset(ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

class StudentViewset(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

""" API """
class FieldAPIViewset(ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldAPISerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

class RoleAPIViewset(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleAPISerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

class WorkerAPIViewset(ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerAPISerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

class StudentAPIViewset(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentAPISerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


""" Authentification Views """
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'message': "Ro'yhatdan muvaffaqiyatli o'tdingiz"}, status=HTTP_201_CREATED)

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token = get_tokens_for_user(user)
            return Response({
                'token': token,
                'message': 'Tizimga muvaffaqiyatli kirdingiz',
            }, status=HTTP_200_OK)

        else:
            return Response({
                'errors': {
                    'non_field_errors': ["Kiritilgan 'parol' yoki 'email' noto'g'ri"]
                }
            }, status=HTTP_404_NOT_FOUND)

class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'message': "Parol muvaffaqiyatli o'zgartirildi"})

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': "Parolni tiklash uchun link yuborildi. Iltimos emailingizni tekshiring"}, status=HTTP_200_OK)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Parol muvaffaqiyatli yangilandi'})


