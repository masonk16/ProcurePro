from core.models import Tender
from core.serializers import TenderSerializer, UserSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User


class TenderList(generics.ListCreateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TenderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
