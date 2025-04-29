from django.contrib.auth.decorators import login_required, user_passes_test

def role_required(allowed_roles):
    def decorator(view_func):
        decorated_view_func = login_required(
            user_passes_test(lambda user: user.role in allowed_roles)(view_func)
        )
        return decorated_view_func
    return decorator
