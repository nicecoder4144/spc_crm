from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpensesViewsets, PaymentViewsets, AreaViewsets, \
    IncomeViewsets,ExpensesAPIViewsets, PaymentAPIViewsets, AreaAPIViewsets, \
        IncomeAPIViewsets, Worker_PaymentViewset

router = DefaultRouter()
router.register(r'expenses', ExpensesViewsets, 'expenses')
router.register(r'payment', PaymentViewsets, 'payment')
router.register(r'area', AreaViewsets, 'area')
router.register(r'income', IncomeViewsets, 'income')
router.register(r'worker-payment', Worker_PaymentViewset, 'worker-payment')

router.register(r'expenses-api', ExpensesAPIViewsets)
router.register(r'payment-api', PaymentAPIViewsets)
router.register(r'area-api', AreaAPIViewsets)
router.register(r'income-api', IncomeAPIViewsets)

urlpatterns = [
    path('', include(router.urls)),
]

