# myApp/decorators.py

from functools import wraps
from django.shortcuts import redirect

def frontend_admin_required(view_func):
    """
    Checks if a front-end admin is logged in via session.
    Redirects to signin page if not.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'frontend_admin_id' not in request.session:
            return redirect('signin')
        return view_func(request, *args, **kwargs)
    return _wrapped_view