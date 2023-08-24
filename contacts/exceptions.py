from rest_framework.exceptions import APIException


class ContactNotFound(APIException):
    status_code = 404
    default_detail = 'Contact not found.'
