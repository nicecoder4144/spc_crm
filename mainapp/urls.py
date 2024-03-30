from django.urls import path, include

from rest_framework import routers

from .views import BranchViewset, RoomViewset, Groupviewset, \
    BranchAPIListview, RoomAPIListview, GroupAPIListview, BranchAPIDetailview, \
    GroupAPIDetailView


router = routers.DefaultRouter()
router.register(r'branch', BranchViewset, 'branch')
router.register(r'room', RoomViewset, 'room')
router.register(r'group', Groupviewset, 'group')

urlpatterns = [
    path('', include(router.urls)),
    path('branch-api/<slug:slug>/', BranchAPIDetailview.as_view()),
    # path('branch-api/<int:id>/', BranchAPIDetailview.as_view()),
    path('branch-api/', BranchAPIListview.as_view()),
    path('room-api/', RoomAPIListview.as_view()),
    path('group-api/', GroupAPIListview.as_view()),

    path('group-detail-api/<str:slug>/', GroupAPIDetailView.as_view(), name="group-detail"),

]


