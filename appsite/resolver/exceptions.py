from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class ResourceExistsError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Target resource exists.')
    default_code = 'target_resource_exists'
