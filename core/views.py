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
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm


# Get the Custom User model
User = get_user_model()


def index(request):
    """
    View to return the landing page.
    """
    return render(request=request, template_name="landing-page.html")


def blog_one(request):
    return render(request=request, template_name="blog-one.html")


def blog_two(request):
    return render(request=request, template_name="blog-two.html")


def blog_three(request):
    return render(request=request, template_name="blog-three.html")


def register_user(request):
    """
    View to handle User registration with the custom user form.
    """
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            selected_group = form.cleaned_data["user_type"]
            group = Group.objects.get(name=selected_group)
            user.groups.add(group)
            messages.success(request, "Registration successful.")
            return redirect("/login/")
    else:
        messages.error(request, "Unsuccessful registration. Invalid information.")
        form = NewUserForm()
    return render(
        request=request, template_name="sign-up.html", context={"register_form": form}
    )


def user_login(request):
    """
    View to handle user authentication (login) using the built-in Authentication Form.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(
                email=email,
                password=password,
            )
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {email}.")
                return redirect("/tenders/")
            else:
                messages.error(request, "Invalid username or password.1")
        else:
            messages.error(request, "Invalid username or password.2")
    form = AuthenticationForm()
    return render(
        request=request, template_name="sign-in.html", context={"login_form": form}
    )


def user_logout(request):
    """
    View to handle logout route.
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:index")


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "tenders": reverse("tender-list", request=request, format=format),
            "bids": reverse("bid-list", request=request, format=format),
        }
    )


class UserList(LoginRequiredMixin, generics.ListAPIView):
    """
    View to list all users.
    """

    login_url = "/login/"
    redirect_field_name = "login"

    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = UserSerializer
    template_name = "users.html"

    def get(self, request, *args, **kwargs):
        """
        Gets a list of all the Users saved in the Users table.
        """
        return Response({"users": User.objects.all()})


class UserDetail(LoginRequiredMixin, generics.RetrieveAPIView):
    """
    View to get individual user details.
    """

    login_url = "/login/"
    redirect_field_name = "login"

    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = UserSerializer
    template_name = "profile.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get(self, request, *args, **kwargs):
        """
        Get user details using the primary key (pk) passed as a parameter.
        """
        self.object = self.get_object()
        return Response({"user": self.object})


class CreateTender(LoginRequiredMixin, views.APIView):
    """
    View to handle Tender creation.
    """

    login_url = "/login/"
    redirect_field_name = "login"

    queryset = Tender.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tender.html"

    def get(self, request, format=None):
        """
        Renders form for Tender creation using the Tender Serializer.
        """
        serializer = TenderSerializer()
        return Response({"serializer": serializer})

    def post(self, request, format=None):
        """
        Saves the Tender to the Tender model using the Tender Serializer.
        """
        # Data dictionary to pass to the serializer.
        category = request.data["category"]
        notice_number = request.data["notice_number"]
        tender_name = request.data["tender_name"]
        requirement_details = request.data["requirement_details"]
        budget = request.data["budget"]
        deadline = request.data["deadline"]
        data = {
            "category": category,
            "notice_number": notice_number,
            "tender_name": tender_name,
            "requirement_details": requirement_details,
            "budget": budget,
            "deadline": deadline,
        }
        serializer = TenderSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return redirect("/tenders/")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTenderList(LoginRequiredMixin, generics.ListAPIView):
    """
    View to display list of all Tenders created by the currently authenticated user.
    """

    login_url = "/login/"
    redirect_field_name = "login"

    queryset = Tender.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer = TenderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    template_name = "my-tenders.html"

    def get(self, owner):
        """
        Returns a list of all the Tenders for the currently authenticated user.
        """
        user = self.request.user
        tenders = Tender.objects.filter(owner=user)
        return Response({"tenders": tenders})


class TenderList(LoginRequiredMixin, generics.ListAPIView):
    """
    View to display a list of all Tenders created by all users.
    """

    login_url = "/login/"
    redirect_field_name = "login"

    queryset = Tender.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer = TenderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    template_name = "tenders-listing.html"

    def get(self, request, *args, **kwargs):
        """
        Returns a list of all the Tenders created by all users.
        """
        return Response({"tenders": Tender.objects.all()})


class TenderDetail(LoginRequiredMixin, generics.ListCreateAPIView):
    """
    View to display details/information for a single Tender.
    """

    login_url = "/login/"
    redirect_field_name = "login"

    queryset = Tender.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = TenderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    template_name = "tender-details.html"

    def get(self, request, pk, *args, **kwargs):
        """
        Returns details for a single Tender.
        :param pk: ID for the Tender to be returned.
        """
        tender = Tender.objects.filter(id=pk)
        return Response({"tender": tender})


class UserTenderDetail(LoginRequiredMixin, generics.ListCreateAPIView):
    """
    View to display details for a specific Tender created by the
    currently authenticated user including Bids placed by Suppliers.
    """

    login_url = "/login/"
    redirect_field_name = "login"

    queryset = Tender.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = TenderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    template_name = "user-tender-details.html"

    def get(self, request, pk, *args, **kwargs):
        """
        Get tender details using the primary key (pk) passed as a parameter.
        param pk: ID for Tender information to be returned.
        return: Tender details including Bids placed for that specific Tender.
        """
        tenders = Tender.objects.filter(id=pk)
        bids = Bids.objects.filter(tender_id=pk)
        return Response({"tenders": tenders, "bids": bids})


class CreateBid(LoginRequiredMixin, views.APIView):
    """
    View to handle Bid creation.
    """

    login_url = "/login/"
    redirect_field_name = "login"

    serializer_class = BidSerializer
    queryset = Bids.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "bidding.html"

    def get(self, request, format=None):
        """
        Renders form for Bid creation using the Bid Serializer.
        """
        serializer = BidSerializer()
        return Response({"serializer": serializer})

    def post(self, request, format=None):
        """
        Saves the Bid to the Tender model using the Bid Serializer.
        """
        # Data dictionary to pass to the serializer.
        description = request.data["description"]
        bid_price = request.data["bid_price"]
        tender_id = request.data["tender_id"]
        data = {
            "description": description,
            "bid_price": bid_price,
            "tender_id": tender_id,
        }
        serializer = BidSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return redirect("/user/bids/")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserBidsList(LoginRequiredMixin, generics.ListAPIView):
    """
    View to display a list of all Bids created by the currently authenticated user.
    """

    login_url = "/login/"
    redirect_field_name = "login"

    queryset = Bids.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer = BidSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    template_name = "bids-listing.html"

    def get(self, owner):
        """
        This view should return a list of all the Tenders for the currently authenticated user.
        :param owner: Email of currently authenticated user.
        """
        user = self.request.user
        bids = Bids.objects.filter(owner=user)
        return Response({"bids": bids})


class BidDetail(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    View to display details for a specific Bid.
    """

    login_url = "/login/"
    redirect_field_name = "login"

    queryset = Bids.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, pk, *args, **kwargs):
        """
        Get bid details using the primary key (pk) passed as a parameter.
        :param pk: ID for Bid information to be returned.
        :return: Bid details.
        """
        bids = Bids.objects.filter(id=pk)
        return Response({"bids": bids}, template_name="bid-details.html")
