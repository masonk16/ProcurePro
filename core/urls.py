from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from core import views

app_name = "main"


# API endpoints
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('apis/', views.api_root),
    path('tender/',
         views.TenderList.as_view(),
         name='tender-list'),
    path('tender/create/',
         views.CreateTender.as_view(),
         name='tender-create'),
    path('tender/<int:pk>/',
         views.TenderDetail.as_view(),
         name='tender-detail'),
    path('bids/',
         views.BidList.as_view(),
         name='bid-list'),
    path('bids/create/',
         views.CreateBid.as_view(),
         name='bid-create'),
    path('bids/<int:pk>/',
         views.BidDetail.as_view(),
         name='bid-detail'),
    path('users/',
         views.UserList.as_view(),
         name='user-list'),
    path('users/<int:pk>/',
         views.UserDetail.as_view(),
         name='user-detail'),
   ]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
