from database.models import *
from passlib.hash import pbkdf2_sha256
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .session import *


def login_user_response(request=None, redir=None):
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST.get('email').lower())
            if pbkdf2_sha256.verify(request.POST.get('password'), user.password):
                if redir:
                    print(redir)
                    response = redirect(redir)
                else:
                    response = redirect('/dashboard/account/profile/')
                session_string = session_create(user, request)

                if request.POST.get('rme') == 'on':
                    response.set_cookie(key="YOJAKA", value=session_string, max_age=(60 * 60 * 24))
                else:
                    response.set_cookie(key="YOJAKA", value=session_string, max_age=None)
                return response
            else:
                return render(request, 'create_login_logout/login.html',
                              dict(failed=True, email=request.POST.get('email')))
        except ObjectDoesNotExist:
            return render(request, 'create_login_logout/login.html',
                          dict(failed=True, email=request.POST.get('email')))
    else:
        return render(request, 'create_login_logout/login.html', {})
