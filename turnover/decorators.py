from django.core.exceptions import PermissionDenied
from functools import wraps


def user_is_manager(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name='Managers').exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
