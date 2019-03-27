from django.shortcuts import render, redirect
from .login import *
from .session import session_check
from .create import *


# Create your views here.

def login_view(request, redir=None):
    if session_check(request)[0]:
        if redir:
            return redirect(redir)
        else:
            return redirect('/dashboard/account/profile')

    return login_user_response(request, redir)


def create_view(request, redir=None):
    if session_check(request)[0]:
        if redir:
            return redirect(redir)
        else:
            return redirect('/dashboard/account/profile')
    return create_user_response(request, redir)


def logout_view(request, redir=None):
    if redir:
        return redirect(redir)
    response = redirect('login')
    if session_delete(request, response):
        response.delete_cookie('YOJAKA')
    return response
