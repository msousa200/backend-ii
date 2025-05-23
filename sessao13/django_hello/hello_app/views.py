"""
Views for hello_app.
"""
import logging
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


logger = logging.getLogger(__name__)

def index(request):
    """Simple Hello World view with JsonResponse."""
    logger.info("Hello World endpoint called")
    return JsonResponse({"message": "Hello from Django"})

@api_view(['GET'])
def hello_api(request):
    """Hello World API view using DRF."""
    logger.info("Hello API endpoint called")
    return Response(
        {"message": "Hello from Django REST Framework"},
        status=status.HTTP_200_OK
    )
