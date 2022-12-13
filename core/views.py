from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from core.models import Tender
from core.serializers import TenderSerializer


@csrf_exempt
def tender_list(request):
    """
    List all Tenders, or create a new tender.
    """
    if request.method == "GET":
        tender = Tender.objects.all()
        serializer = TenderSerializer(tender, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = TenderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def tender_detail(request, pk):
    """
    Retrieve, update or delete a tender.
    """
    try:
        tender = Tender.objects.get(pk=pk)
    except Tender.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TenderSerializer(tender)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TenderSerializer(tender, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        tender.delete()
        return HttpResponse(status=204)
    