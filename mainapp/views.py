from django.shortcuts import render
from pprint import pprint

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, BaseThrottle, ScopedRateThrottle

from .models import Branch, Room, Group
from .serializers import BranchSerializer, RoomSerializer, GroupSerializer,\
    BranchAPISerializer, RoomAPISerializer, GroupAPISerializer, GroupAPIDetailSerializer

# Create your views here.
""" CRUD API  """


class BranchViewset(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'branch_trottle'

    permission_classes = [AllowAny]
    lookup_field = 'slug'

    """ CRUD functions """

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
        except:
            return Response({'error': "Ma'lumotni olishda xatolik yuzaga keldi !!!"})

        try:
            new_branch = Branch.objects.create(
                name=data['name'],
                adress=data['adress'],
                status=data['status'],
            )
            new_branch.save()
            serializer = BranchSerializer(new_branch)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': "Ma'lumotni saqlashda xatolik yuzaga keldi !!!"},
                            status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = self.get_object()
        request_data = request.data

        try:
            data.name = request_data['name'] if 'name' in request_data else data.name
            data.adress = request_data['adress'] if 'adress' in request_data else data.adress
            data.status = request_data['status'] if 'status' in request_data else data.status
            data.save()
            serializer = BranchSerializer(data)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': "Ma'lumot saqlashda hatolik yuzaga keldi !!!"})

    def destroy(self, request, *args, **kwargs):
        data = self.get_object()
        data.delete()
        return Response({'mesage': "Ma'lumot muvaffaqiyatli o'chirildi"}, status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        data = self.get_object()
        new_data = {}

        new_data['id'] = data.id
        new_data['name'] = data.name
        new_data['adress'] = data.adress
        serializer = BranchSerializer(new_data)
        return Response(serializer.data)


class RoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        request_data = request.data
        try:
            branch = Branch.objects.get(id=int(request_data['branch']))
        except:
            return Response({'error': "Bunday Filial topilmadi !"})

        try:
            new_room = Room.objects.create(
                branch=branch,
                number=request_data['number'],
                capacity=request_data['capacity'],
                status=request_data['status'],
            )
            new_room.save()
            serializer = RoomSerializer(new_room)
            return Response(serializer.data)
        except:
            return Response({'error': "Ma'lumot saqlashda xatolik yuzaga keldi !!!"})

    def update(self, request, *args, **kwargs):
        data = self.get_object()
        request_data = request.data
        try:
            if 'branch' in request_data:
                branch = Branch.objects.get(id=request_data['branch'])
            # else:
            #     branch = None
        except:
            return Response({'error': "Bunday Filial topilmadi !"})
        try:
            data.branch = branch if 'branch' in request_data else data.branch
            data.number = request_data['number'] if 'number' in request_data else data.number
            data.capacity = request_data['capacity'] if 'capacity' in request_data else data.capacity
            data.status = request_data['status'] if 'status' in request_data else data.status
            data.save()
            serializer = RoomSerializer(data)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': "Ma'lumot saqlashda xatolik yuzaga keldi !!!"})

    def destroy(self, request, *args, **kwargs):
        data = self.get_object()
        data.delete()
        return Response({'message': "Ma'lumot o'chirildi"}, status.HTTP_204_NO_CONTENT)


class Groupviewset(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


""" API """


class BranchAPIListview(ListAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchAPISerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]  # filter parametrlari
    filterset_fields = ['name', 'adress', 'status',
                        'groups__name']  # filter parametrlari


class BranchAPIDetailview(RetrieveAPIView):
    queryset = Branch.objects.filter(status=True)
    serializer_class = BranchAPISerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    # lookup_field = 'id'


class RoomAPIListview(ListAPIView):
    queryset = Room.objects.filter(status=True)
    serializer_class = RoomAPISerializer
    permission_classes = [AllowAny]


class GroupAPIListview(ListAPIView):
    queryset = Group.objects.filter(status=True)
    serializer_class = GroupAPISerializer
    permission_classes = [AllowAny]


class GroupAPIDetailView(RetrieveAPIView):
    queryset = Group.objects.filter(status=True)
    serializer_class = GroupAPIDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get(self, request, slug, *args, **kwargs):

        group = Group.objects.get(slug=slug)
        serializer = GroupAPIDetailSerializer(group)
        return Response(serializer.data)
