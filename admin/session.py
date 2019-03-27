import secrets
from database.models import *
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def session_create(user=None, request=None):
    temp_session = UserSessionsData()
    temp_stelemetry = SessionTelemetry()
    temp_session.uid = user
    temp_session.session_string = secrets.token_urlsafe(128)
    temp_session.session_delete_string = secrets.token_urlsafe(128)
    temp_stelemetry.ua = request.META.get('HTTP_USER_AGENT', '')
    temp_stelemetry.ip = get_client_ip(request)
    temp_stelemetry.last_active = timezone.now()
    temp_stelemetry.save()
    temp_session.session_telemetry = temp_stelemetry
    temp_session.session_create_time = timezone.now()
    temp_session.session_exp_time = timezone.now() + timedelta(hours=24)
    temp_session.save()
    return temp_session.session_string


def session_check(request=None):
    if request.COOKIES.get('YOJAKA'):
        try:
            temp_session = UserSessionsData.objects.get(session_string=request.COOKIES.get('ADMIN-YOJAKA'))
            if temp_session.session_exp_time < timezone.now():
                # delete the session objec
                temp_session.delete()
                print('fail')
                return False, False
            else:
                temp_session.session_telemetry.last_active = timezone.now()
                temp_session.session_telemetry.ip = get_client_ip(request)
                temp_session.session_telemetry.save()
                return temp_session.uid, temp_session.session_delete_string
        except ObjectDoesNotExist:
            print('fail')
            return False, False
    else:
        return False, False


def session_delete(request=None):
    if request.COOKIES.get('YOJAKA'):
        try:
            temp_session = UserSessionsData.objects.get(session_string=request.COOKIES.get('YOJAKA'))
            if temp_session.session_exp_time < timezone.now():
                # delete the session objec
                temp_session.delete()
                return True
            else:
                if temp_session.session_delete_string == request.POST.get('logout_string'):
                    temp_session.delete()
                    return True
                else:
                    return False
        except ObjectDoesNotExist:
            return True
    else:
        return False
