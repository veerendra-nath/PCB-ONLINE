from database.models import *
from django.shortcuts import render, redirect
from passlib.hash import pbkdf2_sha256


def edit_address(request, user, temp_address):
    temp_address.nick_name = request.POST.get('nick_name')
    temp_address.contact_person_name = request.POST.get('person_name')
    temp_address.company_name = request.POST.get('company_name')
    temp_address.address_line1 = request.POST.get('add_line1')
    temp_address.address_line2 = request.POST.get('add_line2')
    temp_address.city = request.POST.get('city')
    temp_address.state = request.POST.get('state')
    temp_address.pincode = request.POST.get('pincode')
    temp_address.mobile_number = request.POST.get('phone_number')
    temp_address.land_mark = request.POST.get('land_mark')
    temp_address.save()
    user.addresses.add(temp_address)
    user.save()


def addresses_response(request, user, logout_string):
    errors = {}
    status = {'logout_string': logout_string, 'address_objects': user.addresses.all(), 'user': user}
    if request.method == 'POST':
        cmd = request.POST.get('cmd')
        if cmd == "del":
            temp_address = user.addresses.get(id=request.POST.get('add_id'))
            temp_address.delete()
            return redirect(request.path)
        elif cmd == "new":
            temp_address = Addresses()
            edit_address(request, user, temp_address)
            return redirect(request.path)
        elif cmd == "edit":
            temp_address = Addresses.objects.get(id=request.POST.get('add_id'))
            edit_address(request, user, temp_address)
            return redirect(request.path)
        elif cmd == "mk_default":
            temp_address = user.addresses.get(id=request.POST.get('add_id'))
            user.default_address = temp_address
            user.save()
            return redirect(request.path)

    else:
        return render(request, 'dashboard/account/address.html', {'errors': errors, 'status': status})


def password_response(request, user, logout_string):
    errors = {}
    status = {'logout_string': logout_string}
    if (request.method == "POST") and (request.POST.get('new_password1') is not None):
        if request.POST.get('new_password1') == request.POST.get('new_password2'):
            if pbkdf2_sha256.verify(request.POST.get('old_password'), user.password):
                user.password = request.POST.get('new_password1')
                print(user.first_name)
                print(user.last_name)
                user.save(save_pass=True)
                errors['changepass'] = True
                return render(request, 'dashboard/account/password.html', {'errors': errors, 'status': status})
            else:
                errors['passerr'] = True
                return render(request, 'dashboard/account/password.html', {'errors': errors, 'status': status})
        else:
            errors['passequalerr'] = True
            return render(request, 'dashboard/account/password.html', {'errors': errors, 'status': status})
    else:
        return render(request, 'dashboard/account/password.html', {'errors': errors, 'status': status})


def profile_response(request, user, logout_string):
    if isinstance(user, User):
        errors = {}
        status = {'logout_string': logout_string}
        if request.method == 'POST':
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.middle_name = request.POST.get('middle_name')
            user.email = request.POST.get('email')
            user.company_name = request.POST.get('company_name')
            user.gst_number = request.POST.get('gst_number')
            user.phone_number = request.POST.get('phone_number')
            user.save()
        status['user'] = user
        return render(request, 'dashboard/account/profile.html', {'errors': errors, 'status': status})
    else:
        pass
