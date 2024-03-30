from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Expenses, Payment, Area, Income, Worker_Payment
from .serializers import ExpensesSerializer, PaymentSerializer, IncomeSerializer, \
    AreaSerializer, ExpensesAPISerializer, PaymentAPISerializer, IncomeAPISerializer,\
        AreaAPISerializer, Worker_PaymentSerializer

from userapp.models import Worker

# Create your views here.

""" CRUD API """
class ExpensesViewsets(ModelViewSet):
    queryset =  Expenses.objects.all()
    serializer_class = ExpensesSerializer
    permission_classes= [AllowAny]
    lookup_field = 'slug'

class PaymentViewsets(ModelViewSet):
    queryset =  Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes= [AllowAny]

class AreaViewsets(ModelViewSet):
    queryset =  Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes= [AllowAny]
    lookup_field = 'slug'

class IncomeViewsets(ModelViewSet):
    queryset =  Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes= [AllowAny]
    lookup_field = 'slug'

class Worker_PaymentViewset(ModelViewSet):
    queryset = Worker_Payment.objects.all()
    serializer_class = Worker_PaymentSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        request_data = request.data
        x_time = request_data['year'][:7]
        x_time += '-01'
        try:
            worker = Worker.objects.get(id=request_data['worker'])
        except:
            return Response({'error':"Bunday ishchi topilmadi !!!"})

        try:
            new_worker_payment = Worker_Payment.objects.create(
                worker  = worker,
                year = x_time,
                amount = request_data['amount'],
                status = True
            )
            new_worker_payment.save()
            serializer = Worker_PaymentSerializer(new_worker_payment)
        except Exception as e:
            return Response({'error': "Ma'lumot saqlashda xatolik !!!"})
        return Response(serializer.data)

""" API """
class ExpensesAPIViewsets(ModelViewSet):
    queryset =  Expenses.objects.all()
    serializer_class = ExpensesAPISerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

class PaymentAPIViewsets(ModelViewSet):
    queryset =  Payment.objects.all()
    serializer_class = PaymentAPISerializer
    permission_classes= [AllowAny]

class AreaAPIViewsets(ModelViewSet):
    queryset =  Area.objects.all()
    serializer_class = AreaAPISerializer
    permission_classes= [AllowAny]
    lookup_field = 'slug'

class IncomeAPIViewsets(ModelViewSet):
    queryset =  Income.objects.all()
    serializer_class = IncomeAPISerializer
    permission_classes= [AllowAny]
    lookup_field = 'slug'

