from django.db import models
from django.utils import timezone


# Create your models here.
class PaytmTransations(models.Model):
    amount = models.FloatField()
    custemer_id = models.IntegerField()
    is_made = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    is_checksum_valid = models.BooleanField(null=True, blank=True)
    txn_id = models.CharField(null=True, blank=True, max_length=120)
    bank_txn_id = models.CharField(null=True, blank=True, max_length=120)
    status = models.CharField(null=True, blank=True, max_length=120)
    resp_code = models.CharField(null=True, blank=True, max_length=120)
    resp_msg = models.CharField(null=True, blank=True, max_length=120)
    gateway = models.CharField(null=True, blank=True, max_length=120)
    bank_name = models.CharField(null=True, blank=True, max_length=120)
    payment_mode = models.CharField(null=True, blank=True, max_length=120)
    bin = models.CharField(null=True, blank=True, max_length=120)
    card_last_numbers = models.CharField(null=True, blank=True, max_length=120)
    time_stamp = models.DateTimeField(default=timezone.now)

