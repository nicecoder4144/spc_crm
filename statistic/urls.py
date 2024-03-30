from django.urls import path, include
from rest_framework import routers
from .views import Workers_Selery_Stat_Viewset, Input_and_output_Viewset, Quantity_Viewset

router = routers.DefaultRouter()
router.register("workers-salary", Workers_Selery_Stat_Viewset, 'workers-salary')
router.register("input-output", Input_and_output_Viewset, 'input-output')
router.register('quantity', Quantity_Viewset, 'quantity')


urlpatterns = [
    path('', include(router.urls))
]

