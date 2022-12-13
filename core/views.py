from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import Tender
from core.serializers import TenderSerializer


@api_view(['GET', 'POST'])
def tender_list(request, format=None):
    """
    List all Tenders, or create a new tender.
    """
    if request.method == "GET":
        tender = Tender.objects.all()
        serializer = TenderSerializer(tender, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = TenderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def tender_detail(request, pk, format=None):
    """
    Retrieve, update or delete a tender.
    """
    try:
        tender = Tender.objects.get(pk=pk)
    except Tender.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TenderSerializer(tender)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TenderSerializer(tender, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tender.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    