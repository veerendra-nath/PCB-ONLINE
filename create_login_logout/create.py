from django.http import HttpResponseServerError
from database.models import *
from .emails import email_verify
from .session import session_create

from django.shortcuts import render, redirect


def create_user_response(request=None, redir=None):
    errors = {'atc': 0, 'email': 0, 'first_name': 0, 'last_name': 0, 'password': 0, 'company': 0}
    print(errors)
    if request.method == 'POST':
        user = User()
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.middle_name = request.POST.get('middle_name')
        user.email = request.POST.get('email').lower()
        user.company_name = request.POST.get('company')
        user.gst_number = request.POST.get('gst')
        user.password = request.POST.get('password')
        if request.POST.get('atc') != 'on':
            errors['atc'] = 1
            return render(request, 'create_login_logout/create.html', {'user': user, 'errors': errors})
        else:
            validate_errors = user.validate()
            if not validate_errors:
                try:
                    user.save(save_pass=True)
                except:
                    return HttpResponseServerError()
            else:
                for error in validate_errors:
                    errors[error] = 1
                    print(error)
                return render(request, 'create_login_logout/create.html', {'user': user, 'errors': errors})
            if redir:
                response = redirect(redir)
            else:
                response = redirect('dashboard_account', sub_path='profile')
            v = email_verify(type='verification',user=user)
            session_string = session_create(user=user, request=request)
            response.set_cookie(key="YOJAKA", value=session_string, max_age=None)
            return response
    else:
        return render(request, 'create_login_logout/create.html', {'errors': errors})
