from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from core import views

urlpatterns = [
    path('tender/', views.TenderList.as_view()),
    path('tender/<int:pk>', views.TenderDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
