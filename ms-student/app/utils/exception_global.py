import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist, ValidationError

logger = logging.getLogger(_name_)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        return response
    view = context.get('view', None)
    view_name = view._class.name_ if view else 'Unknown'
    if isinstance(exc, ObjectDoesNotExist):
        logger.warning(f"{view_name} - Resource not found: {str(exc)}")
        return Response(
            {"error": "Resource not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    if isinstance(exc, ValidationError):
        logger.warning(f"{view_name} - Validation error: {exc.message_dict if hasattr(exc, 'message_dict') else str(exc)}")
        errors = exc.message_dict if hasattr(exc, 'message_dict') else {"error": str(exc)}
        return Response(
            errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
    if isinstance(exc, ValueError):
        logger.warning(f"{view_name} - Value error: {str(exc)}")
        return Response(
            {"error": str(exc)},
            status=status.HTTP_400_BAD_REQUEST,
        )
    logger.error(
        f"{view_name} - Unhandled exception: {str(exc)}",
        exc_info=True,
        extra={'context': context}
    )
    return Response(
        {"error": "An unexpected error occurred"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
