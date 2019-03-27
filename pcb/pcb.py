import uuid, os, zipfile, re
from .models import *
from database.models import *
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from payments.paytm import paytm_create_request


def gerber_files_identifier(identified_files, file_names):
    solder_mask_top_bits = '^.*\.((dks)|(mks)|(lks))$'
    solder_mask_bottom_bits = '^.*\.((gbs)|(bsm)|(sts))$'
    slick_screen_top_bits = '^.*\.((gto)|(plc)|(tsk))$'
    slick_screen_bottom_bits = '^.*\.((gbo)|(bsk)|(pls))$'
    copper_layer_top_bits = '^.*\.((gbl)|(cmp)|(top))$'
    copper_layer_bottom_bits = '^.*\.((gtl)|(sol)|(bot))$'
    copper_layer_inner_bits = ('ly\d', 'g\d', 'in\d')
    outline_bits = '^.*\.((dim)|(gko))$'
    mechanical_bits = ('gml', 'gm\d')
    dril_plated_bits = '^.*\.((txt)|(tap)|(xln)|(drd)|(exc)|(drl))$'
    drill_non_plated_bits = ()
    # TODO: make regex strings instead of basic string
    for file_name in file_names:
        re_com = re.compile(solder_mask_top_bits)
        if re_com.match(file_name):
            identified_files['solder_masks'] = {'top': file_name}
            continue
        re_com = re.compile(solder_mask_bottom_bits)
        if re_com.match(file_name):
            identified_files['solder_masks'] = {'bottom': file_name}
            continue
        re_com = re.compile(slick_screen_top_bits)
        if re_com.match(file_name):
            identified_files['slick_screens'] = {'top': file_name}
            continue
        re_com = re.compile(slick_screen_bottom_bits)
        if re_com.match(file_name):
            identified_files['slick_screens'] = {'bottom': file_name}
            continue


def pcb_upload_response(request, user, logout_string):
    # TODO: check post method has given data
    # TODO: save post zip file in local /tmp storage
    # TODO: extract the zip files
    # TODO: parse the gerber file extensions (multiple extension are there )
    # TODO: parse the gerber file extensions  version 2
    # TODO: call gerbv external c call and parse response
    # TODO: render the gerber file layer by layer and combine
    # TODO: check basic errors like no soldermask , no slick screen odd copper layer , errors in d code of gerfile
    # TODO: report errors , like zip file size error , over sized zip file
    status = {'logout_string': logout_string}
    if request.method == "POST" and request.FILES['gerber_archive']:
        archive_file = request.FILES['gerber_archive']
        # print(dir(archive))
        # print(archive.name)
        if not (zipfile.is_zipfile(archive_file)):
            print("not zip")
        else:
            zip_archive_instance = zipfile.ZipFile(archive_file)
            gerber = GerberFiles()
            gerber.set_user_email(user.email)
            '''identified_files={'unknown_files':[],'solder_masks':None,'slick_screens':None,'copper_layers':None,'outline_cuts':None,'dril_files':None}
            for file_name in zip_archive_instance.namelist():
                #TODO: extract extensions method one 
                #TODO: remove extension identify by name
                gerber_files_identifier(identified_files,file_name)
            random_path='/tmp/{0}/'.format(uuid.uuid1().hex)
            #TODO:list the files before extracts , identify by the extension name , it self here 
            archive_instance.extractall(path=random_path)
            #TODO: have to inspect the pcb items ,extension inception  here'''
            # FIXME: For present no rendering identify the  call the gerbv for render and identify the dimensiions

            gerber.archive_file = archive_file
            gerber.save()
            order = PCBOrders()
            order.user = user
            order.transaction_uuid = uuid.uuid1()
            order.gerber_files = gerber
            order.save()
            return redirect('pcb_properties_selection', transaction_uuid=order.transaction_uuid)
    else:
        return render(request, 'pcb/pcb_upload.html', status)


def pcb_properties_selection_response(request, user, logout_string, transaction_uuid):
    try:
        order = PCBOrders.objects.get(transaction_uuid=transaction_uuid)
    except ObjectDoesNotExist:
        return redirect('pcb_upload')
    if order.user != user:
        return redirect('pcb_upload')
    if order.is_paid:
        return 0
    if request.method != 'POST':
        status = {'available_properties': {'materials': PCBMaterials.objects.all(),
                                           'layers': PCBCULayers.objects.all(),
                                           'thicknesses': PCBThicknesses.objects.all(),
                                           'cu_thicknesses': PCBCUThicknesses.objects.all(),
                                           'surface_finishes': PCBSurfaceFinishes.objects.all(),
                                           'colors': PCBColors.objects.all(),
                                           'ss_colors': PCBSSColors.objects.all()},
                  'logout_string': logout_string}
        return render(request, 'pcb/pcb_properties_selection.html', status)
    settings = PCBOrderSettings()
    settings.pcb_material = PCBMaterials.objects.get(value=request.POST.get('material'))
    settings.pcb_copper_layers = PCBCULayers.objects.get(value=request.POST.get('cu_layers'))
    settings.pcb_copper_thickness = PCBCUThicknesses.objects.get(value=request.POST.get('cu_thickness'))
    settings.pcb_thickness = PCBThicknesses.objects.get(value=request.POST.get('thickness'))
    settings.pcb_surface_finish = PCBSurfaceFinishes.objects.get(value=request.POST.get('surface_finish'))
    settings.pcb_color_top = PCBColors.objects.get(value=request.POST.get('top_color'))
    settings.pcb_color_bottom = PCBColors.objects.get(value=request.POST.get('bottom_color'))
    settings.pcb_slickscreen_color_top = PCBSSColors.objects.get(value=request.POST.get('ss_top_color'))
    settings.pcb_slickscreen_color_bottom = PCBSSColors.objects.get(value=request.POST.get('ss_bottom_color'))
    settings.pcb_width = request.POST.get('y')
    settings.pcb_length = request.POST.get('x')
    errors = False  # TODO settings.validate()
    if not errors:
        settings.save()
        order.remarks = request.POST.get('remarks')
        order.quantity = request.POST.get('quantity')
        order.order_type = request.POST.get('order_type')
        order.pcb_settings = settings
        # pcb_order.calculate_rate(coupon=request.POST.get('coupon'))
        order.save()
        return redirect('pcb_order', transaction_uuid=transaction_uuid)


def pcb_order_response(request, user, logout_string, transaction_uuid):
    try:
        order = PCBOrders.objects.get(transaction_uuid=transaction_uuid)
    except ObjectDoesNotExist:
        return redirect('pcb_upload')
    if order.user != user:
        return redirect('pcb_upload')
    if order.is_paid:
        return 0
    if not order.pcb_settings:
        return redirect('pcb_properties_selection', transaction_uuid=order.transaction_uuid)

    status = {'selected_properties': {'color_top': order.pcb_settings.pcb_color_top.value,
                                      'color_bottom': order.pcb_settings.pcb_color_bottom.value,
                                      'ss_color_top': order.pcb_settings.pcb_slickscreen_color_top.value,
                                      'ss_color_bottom': order.pcb_settings.pcb_slickscreen_color_bottom.value,
                                      'material': order.pcb_settings.pcb_material.value,
                                      'layers': order.pcb_settings.pcb_copper_layers.value,
                                      'cu_thickness': order.pcb_settings.pcb_copper_thickness.value,
                                      'thickness': order.pcb_settings.pcb_thickness.value,
                                      'surface_finish': order.pcb_settings.pcb_surface_finish.value,
                                      'length': order.pcb_settings.pcb_length,
                                      'width': order.pcb_settings.pcb_width,
                                      'quantity': order.quantity,
                                      'remarks': order.remarks},
              'logout_string': logout_string,
              'payment_url': '/pcb/order/payment/' + str(order.transaction_uuid)}

    return render(request, 'pcb/order_preview.html', status)


def pcb_order_payment_response(request,user, logout_string, transaction_uuid):
    try:
        order = PCBOrders.objects.get(transaction_uuid=transaction_uuid)
    except ObjectDoesNotExist:
        return redirect('pcb_upload')
    if order.user != user:
        return redirect('pcb_upload')
    if order.is_paid:
        return 0
    if not order.pcb_settings:
        return redirect('pcb_properties_selection', transaction_uuid=order.transaction_uuid)
    if request.method == 'POST':
        print(request.POST)
        return None
    order_params = {'id': str(order.id),
                    'uid': str(order.user.id),
                    'amount': order.total_amount,
                    'email': order.user.email,
                    'mobile': order.user.phone_number,
                    'callback_url': 'https://ioproto.com/pcb/order/payment/' + str(order.transaction_uuid)
                    }
    return paytm_create_request(request, order_params)
