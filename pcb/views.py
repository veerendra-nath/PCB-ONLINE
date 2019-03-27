from django.shortcuts import render, redirect
from create_login_logout import session
from .pcb import *
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def pcb_upload_view(request):
    user, delete_string = session.session_check(request)
    if not user:
        return redirect('login_redir', redir=request.path)
    return pcb_upload_response(request, user, delete_string)


def pcb_properties_selection_view(request, transaction_uuid=None):
    user, delete_string = session.session_check(request)
    if not user:
        return redirect('login_redir', redir=request.path)
    return pcb_properties_selection_response(request, user, delete_string, transaction_uuid)


def pcb_order_view(request, transaction_uuid=None):
    user, delete_string = session.session_check(request)
    if not user:
        return redirect('login_redir', redir=request.path)
    return pcb_order_response(request, user, delete_string, transaction_uuid)


@csrf_exempt
def pcb_order_payment(request, transaction_uuid=None):
    user, delete_string = session.session_check(request)
    if not user:
        return redirect('login_redir', redir=request.path)
    return pcb_order_payment_response(request, user, delete_string, transaction_uuid)


def pcb_order_status_view(request, transaction_uuid=None):
    user, delete_string = session.session_check(request)
    if not user:
        return redirect('login_redir', redir=request.path)
    return pcb_upload_gunas_response(request, user, delete_string, transaction_uuid)
