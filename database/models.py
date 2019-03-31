from django.db import models
from django.utils import timezone
from passlib.hash import pbkdf2_sha256
from django.core.exceptions import ValidationError
from django.core.validators import *


# Create your models here.
class Addresses(models.Model):
    nick_name = models.CharField(max_length=50, null=True)
    contact_person_name = models.CharField(max_length=50, null=False, blank=False)
    company_name = models.CharField(max_length=50, null=True)
    address_line1 = models.CharField(max_length=130, null=False, blank=False)
    address_line2 = models.CharField(max_length=120, null=True)
    city = models.CharField(max_length=120, null=True, blank=False)
    state = models.CharField(max_length=120, null=True, blank=False)
    pincode = models.CharField(max_length=20, null=False, blank=False)
    mobile_number = models.CharField(max_length=20, null=False, blank=False)
    land_mark = models.CharField(max_length=20, null=False, default="")

    # uid=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table = 'Addresses'

    def __str__(self):
        return self.nick_name

    def __repr__(self):
        return "add"


class User(models.Model):
    first_name = models.CharField(max_length=50, validators=[
        RegexValidator('^[^0-9]{3,50}$', 'should be 3 or more, max 50 and no numbers', 'validation_failed')])
    last_name = models.CharField(max_length=50, validators=[
        RegexValidator('^[^0-9]{3,50}$', 'should be 3 or more, max 50 and no numbers', 'validation_failed')])
    middle_name = models.CharField(max_length=50, null=True, blank=True, validators=[
        RegexValidator('^[^0-9]{3,50}$', 'should be 3 or more, max 50 and no numbers', 'validation_failed')])
    company_name = models.CharField(max_length=50, null=True, default='', blank=True, validators=[
        RegexValidator('^[^0-9]{3,50}$', 'should be 3 or more, max 50 and no numbers', 'validation_failed')])
    email = models.EmailField(unique=True)
    new_email = models.EmailField(null=True, blank=True, )
    gst_number = models.CharField(max_length=50, null=True, blank=True, default='')
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    addresses = models.ManyToManyField(Addresses, blank=True)
    mail_verified = models.BooleanField(default=False)
    default_address = models.ForeignKey(Addresses, null=True, blank=True, related_name='default_address',
                                        on_delete=models.SET_NULL)
    password = models.CharField(max_length=120, null=False, blank=False, default=None)
    billing_address = models.ForeignKey(Addresses, null=True, blank=True, related_name='billing_address',
                                        on_delete=models.SET_NULL)
    phone_number = models.CharField(max_length=50, null=True, blank=True, default='', validators=[
        RegexValidator('^[0-9+][0-9]{9,20}$', 'should be 10 numbers', 'validation_failed')])

    class Meta:
        db_table = 'Users'

    def save(self, force_insert=False, save_pass=False, force_update=False, **kwargs):
        if not (force_insert or force_update):
            self.full_clean()
        if save_pass:
            hashed_password = pbkdf2_sha256.hash(self.password)
            self.password = hashed_password
        super(User, self).save()

    def validate(self):
        try:
            self.full_clean()
            return False
        except ValidationError as error_string:
            error_dict = {}
            for error in error_string:
                error_dict[error[0]] = error[1][0]
            return error_dict

    def __str__(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name


class VerificationData(models.Model):
    data = models.CharField(max_length=150, null=False,  unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'VerificationData'


class SessionTelemetry(models.Model):
    ua = models.CharField(max_length=500, null=True)
    ip = models.GenericIPAddressField(null=True)
    last_active = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'SessionTelemetry'


class UserSessionsData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_string = models.CharField(max_length=256, null=False)
    session_delete_string = models.CharField(max_length=256, null=False)
    session_create_time = models.DateTimeField(default=timezone.now)
    session_exp_time = models.DateTimeField(default=timezone.now)
    session_telemetry = models.ForeignKey(SessionTelemetry, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'UsersSessionsData'


class TempSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.CharField(max_length=50, null=False)
    session_exp_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'TempSession'


class Coupons(models.Model):
    code = models.CharField(max_length=20, unique=True)
    expiry_date = models.DateTimeField()
    coupon_scope = models.CharField(max_length=3)
    create_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_redeemed = models.BooleanField(default=False)
    max_redemption_per_user = models.IntegerField()
    max_redemption_count = models.IntegerField()
    discount_type = models.CharField(max_length=10)
    max_redemption_amount = models.IntegerField()
    to_avail_minimum_amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=None, null=True, blank=True)

    class Meta:
        db_table = 'Coupons'


class AwsEmailLog(models.Model):
    pass


class UserEmails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=500)
    message = models.CharField(max_length=10480)
    sender = models.CharField(max_length=120)
    replay_to = models.CharField(max_length=120)
    cc = models.CharField(max_length=120)
    bc = models.CharField(max_length=120)

