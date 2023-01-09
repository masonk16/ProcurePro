from django.http import HttpResponseRedirect
from rest_framework.renderers import TemplateHTMLRenderer

from core.models import Tender, Bids
from core.serializers import BidSerializer, TenderSerializer, UserSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import Group
from core.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm
import pprint
User = get_user_model()


def index(request):
    return render(request=request, template_name="index.html")


def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            selected_group = form.cleaned_data['user_type']
            group = Group.objects.get(name=selected_group)
            user.groups.add(group)
            # group.user_set.add(user)
            messages.success(request, "Registration successful.")
            return HttpResponseRedirect('login/')
    else:
        messages.error(request, "Unsuccessful registration. Invalid information.")
        form = NewUserForm()
    return render(request=request, template_name="sign-up.html", context={"register_form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        pprint.pprint(form.data)
        pprint.pprint(form)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password,)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {email}.")
                return redirect('')
            else:
                messages.error(request, "Invalid username or password.1")
        else:
            messages.error(request, "Invalid username or password.2")
    form = AuthenticationForm()
    return render(request=request, template_name="sign-in.html", context={"login_form": form})


def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:index")


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
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response({'users': User.objects.all()}, template_name='users.html')


class UserDetail(generics.RetrieveAPIView):
    """
    Gets individual user details.
    """
    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = UserSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'user': self.object}, template_name='empty.html')


class TenderList(generics.ListCreateAPIView):
    queryset = Tender.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = TenderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        return Response({'tenders': Tender.objects.all()}, template_name='tenders-listing.html')


class TenderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tender.objects.all()
    # renderer_classes = [TemplateHTMLRenderer]
    serializer_class = TenderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]



class BidList(generics.ListCreateAPIView):
    queryset = Bids.objects.all()
    # renderer_classes = [TemplateHTMLRenderer]
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BidDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bids.objects.all()
    # renderer_classes = [TemplateHTMLRenderer]
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

