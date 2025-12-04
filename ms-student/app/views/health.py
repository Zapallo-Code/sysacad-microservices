from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import connection


@api_view(["GET"])
def health_check(request):

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return Response(
            {"status": "healthy", "database": "connected"},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {"status": "unhealthy", "database": "disconnected", "error": str(e)},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
