from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME


def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='home'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.profile.is_admin ,
        login_url=login_url,
        redirect_field_name = redirect_field_name
    )
    if function:
        return actual_decorator(function)
    else:
        return actual_decorator




