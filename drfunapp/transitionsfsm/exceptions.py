from rest_framework.exceptions import APIException


class RequestedOperationFailedException(APIException):
    status_code = 500
    default_detail = 'The requested operation failed.'
