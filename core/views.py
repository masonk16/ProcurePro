from core.models import Tender, Bids
from core.serializers import BidSerializer, TenderSerializer, UserSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from core.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'tenders': reverse('tender-list', request=request, format=format),
        'bids': reverse('bid-list', request=request, format=format)
    })


class UserList(generics.ListAPIView):
    """
    Lists all users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    Gets individual user details.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TenderList(generics.ListCreateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TenderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class BidList(generics.ListCreateAPIView):
    queryset = Bids.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BidDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bids.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

