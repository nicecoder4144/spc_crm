from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FieldViewset, RoleViewset, WorkerViewset, StudentViewset, \
    FieldAPIViewset, RoleAPIViewset, WorkerAPIViewset, StudentAPIViewset, \
    UserRegistrationView, UserLoginView, LogoutAPIView, UserChangePasswordView,\
    SendPasswordResetEmailView, UserPasswordResetView

router = DefaultRouter()
router.register(r'field', FieldViewset)
router.register(r'role', RoleViewset)
router.register(r'worker', WorkerViewset)
router.register(r'student', StudentViewset)

router.register(r'field-api', FieldAPIViewset)
router.register(r'role-api', RoleAPIViewset)
router.register(r'worker-api', WorkerAPIViewset)
router.register(r'student-api', StudentAPIViewset)

urlpatterns = [
    # path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('password-change/', UserChangePasswordView.as_view(), name='password-change'),
    path('password-reset-email/', SendPasswordResetEmailView.as_view(), name='password-reset-email'),
    path('password-reset/<uid>/<token>/', UserPasswordResetView.as_view(), name='password-reset'),
]

