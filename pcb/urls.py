from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.pcb_upload_view, name='pcb_upload'),
    path('gunas/<uuid:transaction_uuid>', views.pcb_properties_selection_view, name="pcb_properties_selection"),
    path('order/<uuid:transaction_uuid>', views.pcb_order_view, name="pcb_order"),
    path('order/status/<uuid:transaction_uuid>', views.pcb_order_status_view, name="pcb_order_status"),
    path('order/payment/<uuid:transaction_uuid>', views.pcb_order_payment, name="pcb_order_payment"),
    # path('order/payment/response/<uuid:transaction_uuid>',views.pay_response),
]
