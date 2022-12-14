from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from core import views

# API endpoints
urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('tender/',
         views.TenderList.as_view(),
         name='tender-list'),
    path('tender/<int:pk>/',
         views.TenderDetail.as_view(),
         name='tender-detail'),
    path('users/',
         views.UserList.as_view(),
         name='user-list'),
    path('users/<int:pk>/',
         views.UserDetail.as_view(),
         name='user-detail')
])
