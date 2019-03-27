from create_login_logout.session import session_check
from .account import *


# Create your views here.
def account_view(request, sub_path):
    user, logout_string = session_check(request)
    if user:
        if sub_path == 'profile':
            return profile_response(request, user, logout_string)
        if sub_path == 'addresses':
            return addresses_response(request, user, logout_string)
        if sub_path == 'password':
            return password_response(request, user, logout_string)
    return redirect('login_redir', redir=request.path)
