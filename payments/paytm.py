from .paytm_checksum import *
from .models import PaytmTransations
from django.shortcuts import render


def paytm_create_request(request, order):
    paytm_order_params = {'MID': 'KTkOnx66876446691339',
                          'CUST_ID': order['uid'],
                          'TXN_AMOUNT': '100',
                          'CHANNEL_ID': 'WEB',
                          'WEBSITE': 'WEBSTAGING',
                          'INDUSTRY_TYPE_ID': 'Retail',
                          'CALLBACK_URL': order['callback_url'],
                          'MOBILE_NO': order['mobile'],
                          'EMAIL': order['email']

                          }

    print(paytm_order_params)
    paytm_transaction = PaytmTransations()
    paytm_transaction.amount = paytm_order_params['TXN_AMOUNT']
    paytm_transaction.custemer_id = paytm_order_params['CUST_ID']
    paytm_transaction.email = paytm_order_params['EMAIL']
    paytm_transaction.mobile_no = paytm_order_params['MOBILE_NO']
    paytm_transaction.save()
    paytm_order_params['ORDER_ID'] = str(paytm_transaction.id)
    paytm_order_params['CHECKSUMHASH'] = generate_checksum(paytm_order_params, 'FzENBs@EW!LDhqCZ')
    return render(request, 'payments/paytm.html', paytm_order_params)


def paytm_check_response(response):
    pass
