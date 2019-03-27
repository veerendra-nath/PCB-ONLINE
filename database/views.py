from django.shortcuts import render
from account.session import *
from .changepass import *
from .address import *
# Create your views here.
def dashboard(request):
    return(render(request,'temp.html',{}))
def password_view(request):
    user=session_check(request)
    if(user):
        if(request.method=='POST'):
            return(password_cahnge(request,user))
        else:
            return(render(request,'password.html',{}))
    else:
        return (redirect('/account?redir=/dashboard/password'))
def profile_view(request):
    user=session_check(request)
    if(user):
        if(request.method=='POST'):
           user.first_name=request.POST.get('first_name')
           user.last_name=request.POST.get('last_name')
           user.middle_name=request.POST.get('middle_name')
           user.email=request.POST.get('email')
           user.company_name=request.POST.get('company_name')
           user.gst_number=request.POST.get('gst_number')
           user.phone_number=request.POST.get('phone_number')
           user.save()
        return(render(request,'profile.html',{'user':user}))
    else:
        return(redirect('/account?redir=/dashboard/profile'))
def address_view(request):
    user=session_check(request)
    if(user):
        if(request.method=='POST'):
            address_operations(request,user)
            return(render(request,'address.html',{'address_objects':user.address.all()}))
        else:
            return(render(request,'address.html',{'address_objects':user.address.all()}))   
    else:
        return(redirect('/account?redir=/dashboard/address'))
    