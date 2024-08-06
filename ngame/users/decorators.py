from django.core.exceptions import PermissionDenied

def user_is_admin(user):
    if user.user_type == "admin":
        return True
    else:
        raise PermissionDenied
    
def user_is_client(user):
    if user.user_type == "client":
        return True
    else:
        raise PermissionDenied