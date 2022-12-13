from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from core import views

urlpatterns = [
    path('tender/', views.tender_list),
    path('tender/<int:pk>', views.tender_detail),
    # path('', home, name='home'),
    # path('login/', login, name='login'),
    # path('logout/', logout, name='logout'),
    # path('register/', register, name='register'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
