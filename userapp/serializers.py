from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import Field, Role, Worker, Student
from .utils import Util
from finance.serializers import Worker_PaymentSerializer, PaymentStudentAPISerializer

""" CRUD API """
class FieldSerializer(ModelSerializer):
    class Meta:
        model = Field
        fields = ('__all__')
        
class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ('__all__')

class WorkerSerializer(ModelSerializer):
    class Meta:
        model = Worker
        fields = ('__all__')

class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ('__all__')

""" API """
class WorkerAPISerializer(ModelSerializer):
    direction_name = serializers.CharField(source='diriction.name')
    direction_slug = serializers.CharField(source='diriction.slug')
    role_name = serializers.CharField(source='role.name')
    role_slug = serializers.CharField(source='role.slug')
    worker_payments = Worker_PaymentSerializer(many=True, read_only=True)
    class Meta:
        model = Worker
        fields = ('id', 'full_name', 'slug', 'phone_number', 'passport', 'percentage', 'salary',\
                  'direction_name', 'direction_slug', 
                  'role_name', 'role_slug',
                  'worker_payments')

class RoleAPISerializer(ModelSerializer):
    workers = WorkerAPISerializer(many=True, read_only = True)
    class Meta:
        model = Role
        fields = ('id', 'name', 'slug', 'workers')

class StudentAPISerializer(ModelSerializer):
    field_name = serializers.CharField(source='field.name')
    field_slug = serializers.CharField(source='field.slug')
    class Meta:
        model = Student
        fields = ('id', 'full_name', 'slug', 'date_of_birth', 'passport', 'phone_number', 'father_name', \
                  'father_phone', 'field_name', 'field_slug', 'day', 'time')

class FieldAPISerializer(ModelSerializer):
    students = StudentAPISerializer(many=True, read_only=True)
    workers = WorkerAPISerializer(many=True, read_only=True)
    class Meta:
        model = Field
        fields = ('id', 'name', 'slug', 'cost', 'duration', 'students', 'workers')

""" For Student paymens info """
class StudentPaymentAPISerializer(ModelSerializer):
    payments = PaymentStudentAPISerializer(many=True, read_only=True)
    class Meta:
        model = Student
        fields = ('id', 'full_name', 'slug', 'day', 'time', \
                  'payments',
                  )


""" Authentification Serializers """
"""
    Ro'yhatdan o'tish;
    Login;
    Logout;
    Password change;
    Password sent email
    Password reset
"""

class UserRegistrationSerializer(serializers.ModelSerializer):
  # Ro'yhatdan o'tish vaqtida parolni tekshirish uchun password2 maydoni yaratib olindi
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = Worker
    fields = (
            "username",
            "password",
            "password2",
            "full_name",
            "role",
            "diriction",
            "phone_number",\
            "passport",
            "percentage",
            "salary",
        )
    extra_kwargs={
      'password':{'write_only':True}
    }

  # parollarni validatsiyadan o'tkazish va bir biriga mosligini tekshirib chiqamiz
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Kiritilgan parollar birxil emas !!!")
    return attrs

  def create(self, validate_data):
    return Worker.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  # login uchun vaqtinchalik 'username' maydonini yaratib olish kerak
  username = serializers.CharField()

  class Meta:
    model = Worker
    fields = ['username', 'password']

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class UserChangePasswordSerializer(serializers.Serializer):
  current_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

  class Meta:
    fields = ['current_password', 'password', 'password2']

  def validate_current_password(self, value):
    user = self.context.get('user')
    if not user.check_password(value):
      raise serializers.ValidationError("Joriy parol noto'g'ri kiritildi !")
    return value

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Kiritilgan yangi parollar bir-biriga mos emas !!!")
    user = self.context.get('user')
    user.set_password(password)
    user.save()
    return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        print(f"attrs ---- {email}")
        
        if Worker.objects.filter(email=email).exists():
            user = Worker.objects.get(email = email)
            print(f"user ---- {user.email}")
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("--------------------------------------------------------------------------------")
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link', link)
            print("-------------------------------------------------------------------------------")
            # Send EMail
            body = 'Parolingizni tiklash uchun quyidagi havolani bosing '+link
            data = {
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError("Siz ro'yhatdan o'tmagansiz")

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = Worker.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')




