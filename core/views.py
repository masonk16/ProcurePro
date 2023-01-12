
from django.http import HttpResponseRedirect
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Tender, Bids
from core.serializers import BidSerializer, TenderSerializer, UserSerializer
from rest_framework import generics, permissions, views, status
from django.contrib.auth.models import Group
from core.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm


User = get_user_model()


def index(request):
    return render(request=request, template_name="landing-page.html")


def blog_one(request):
    return render(request=request, template_name="blog-one.html")


def blog_two(request):
    return render(request=request, template_name="blog-two.html")


def blog_three(request):
    return render(request=request, template_name="blog-three.html")


def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            selected_group = form.cleaned_data['user_type']
            group = Group.objects.get(name=selected_group)
            user.groups.add(group)
            messages.success(request, "Registration successful.")
            return redirect('/login/')
    else:
        messages.error(request, "Unsuccessful registration. Invalid information.")
        form = NewUserForm()
    return render(request=request, template_name="sign-up.html", context={"register_form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password,)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {email}.")
                return redirect('/tenders/')
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


class UserList(LoginRequiredMixin, generics.ListAPIView):
    """
    Lists all users.
    """
    login_url = '/login/'
    redirect_field_name = 'login'

    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = UserSerializer
    template_name = 'users.html'

    def get(self, request, *args, **kwargs):
        return Response({'users': User.objects.all()})


class UserDetail(LoginRequiredMixin, generics.RetrieveAPIView):
    """
    Gets individual user details.
    """
    login_url = '/login/'
    redirect_field_name = 'login'

    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = UserSerializer
    template_name = 'profile.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'user': self.object})


class CreateTender(views.APIView):
    queryset = Tender.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'empty.html'

    def get(self, request, format=None):

        serializer = TenderSerializer()
        return Response({'serializer': serializer})

    def post(self, request, format=None):

        category = request.data['category']
        notice_number = request.data['notice_number']
        tender_name = request.data['tender_name']
        requirement_details = request.data['requirement_details']
        budget = request.data['budget']
        deadline = request.data['deadline']
        data = {
            'category': category,
            'notice_number': notice_number,
            'tender_name': tender_name,
            'requirement_details': requirement_details,
            'budget': budget,
            'deadline': deadline,
        }
        serializer = TenderSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return redirect('/tender/')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTenderList(generics.ListAPIView):
    login_url = '/login/'
    redirect_field_name = 'login'

    queryset = Tender.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer = TenderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    template_name = 'my-tenders.html'

    def get(self, owner):
        """
        This view should return a list of all the Tenders for the currently authenticated user.
        """
        user = self.request.user
        print(user)
        tenders = Tender.objects.filter(owner=user)
        return Response({'tenders': tenders})


class TenderList(generics.ListAPIView):
    login_url = '/login/'
    redirect_field_name = 'login'

    queryset = Tender.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer = TenderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return Response({'tenders': Tender.objects.all()}, template_name='tenders-listing.html')


class TenderDetail(LoginRequiredMixin, generics.ListCreateAPIView):
    login_url = '/login/'
    redirect_field_name = 'login'

    queryset = Tender.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = TenderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk, *args, **kwargs):
        tender = Tender.objects.filter(id=pk)
        return Response({'tender': tender}, template_name='tender-details.html')


class UserTenderDetail(LoginRequiredMixin, generics.ListCreateAPIView):
    login_url = '/login/'
    redirect_field_name = 'login'

    queryset = Tender.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = TenderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk, *args, **kwargs):
        tenders = Tender.objects.filter(id=pk)
        bids = Bids.objects.filter(tender_id=pk)
        return Response({'tenders': tenders, 'bids': bids}, template_name='user-tender-details.html')


class CreateBid(views.APIView):
    # serializer_class = BidSerializer
    queryset = Bids.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'bidding.html'

    def get(self, request, format=None):

        serializer = BidSerializer()
        return Response({'serializer': serializer})

    def post(self, request, format=None):
        description = request.data['description']
        bid_price = request.data['bid_price']
        tender_id = request.data['tender_id']
        data = {
            'description': description,
            'bid_price': bid_price,
            'tender_id': tender_id
        }
        serializer = BidSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return redirect('/user/bids/')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserBidsList(generics.ListAPIView):
    login_url = '/login/'
    redirect_field_name = 'login'

    queryset = Bids.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer = BidSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    template_name = 'bids-listing.html'

    def get(self, owner):
        """
        This view should return a list of all the Tenders for the currently authenticated user.
        """
        user = self.request.user
        print(user)
        bids = Bids.objects.filter(owner=user)
        return Response({'bids': bids})


# class BidList(LoginRequiredMixin, generics.ListCreateAPIView):
#     login_url = '/login/'
#     redirect_field_name = 'login'
#
#     queryset = Bids.objects.all()
#     renderer_classes = [TemplateHTMLRenderer]
#     serializer_class = BidSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#     def get(self, request, *args, **kwargs):
#         return Response({'bids': Bids.objects.all()}, template_name='bids-listing.html')


class BidDetail(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    login_url = '/login/'
    redirect_field_name = 'login'

    queryset = Bids.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get(self, request, pk, *args, **kwargs):
        bids = Bids.objects.filter(id=pk)
        return Response({'bids': bids}, template_name='bid-details.html')
