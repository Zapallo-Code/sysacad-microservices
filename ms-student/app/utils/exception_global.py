import logging

import requests
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        return response
    view = context.get("view", None)
    view_name = view.__class__.__name__ if view else "Unknown"

    # Handle HTTP errors from external microservices
    if isinstance(exc, (requests.Timeout, requests.ConnectionError)):
        logger.error(f"{view_name} - External service unavailable: {str(exc)}")
        return Response(
            {"error": "External service temporarily unavailable. Please try again later."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    if isinstance(exc, requests.HTTPError):
        logger.error(f"{view_name} - External service error: {str(exc)}")
        return Response(
            {"error": "Error communicating with external service"},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    if isinstance(exc, ObjectDoesNotExist):
        logger.warning(f"{view_name} - Resource not found: {str(exc)}")
        return Response(
            {"error": "Resource not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    if isinstance(exc, ValidationError):
        errors = getattr(exc, "message_dict", {"error": str(exc)})
        logger.warning(f"{view_name} - Validation error: {errors}")
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    if isinstance(exc, ValueError):
        logger.warning(f"{view_name} - Value error: {str(exc)}")
        return Response(
            {"error": str(exc)},
            status=status.HTTP_400_BAD_REQUEST,
        )
    logger.error(
        f"{view_name} - Unhandled exception: {str(exc)}", exc_info=True, extra={"context": context}
    )
    return Response(
        {"error": "An unexpected error occurred"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
