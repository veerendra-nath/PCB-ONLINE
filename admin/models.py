from django.db import models
from django.utils import timezone
from passlib.hash import pbkdf2_sha256
from django.core.exceptions import ValidationError

# Create your models here.


class Groups(models.Model):
    is_super_user = models.BooleanField()
    can_create_admin_users = models.BooleanField()
    can_edit_admin_users = models.BooleanField()
    can_edit_normal_users = models.BooleanField()
    can_edit_pcb_properties = models.BooleanField()
    can_edit_order = models.BooleanField()
    can_replay_user = models.BooleanField()


class AdminUser(models.Model):
    user_name = models.CharField(max_length=120)
    full_name = models.CharField(max_length=150)
    is_active = models.BooleanField()
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    password = models.CharField(max_length=120, null=False, blank=False, default=None)
    email = models.EmailField()



    def save(self, force_insert=False, save_pass=False, force_update=False, **kwargs):
        if not (force_insert or force_update):
            self.full_clean()
        if save_pass:
            hased_password = pbkdf2_sha256.hash(self.password)
            self.password = hased_password
        super(AdminUser, self).save()

    def validate(self):
        try:
            self.full_clean()
            return True
        except ValidationError as error_string:
            error_dict = {}
            for error in error_string:
                error_dict[error[0]] = error[1][0]
            return error_dict

    def __str__(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name


class VerificationTypes(models.Model):
    stype = models.CharField(max_length=6, null=False)



class VerificationData(models.Model):
    vdata = models.UUIDField(null=False)
    uid = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    vtype = models.ForeignKey(VerificationTypes, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)




class AdminSessionTelemetry(models.Model):
    ua = models.CharField(max_length=500, null=True)
    ip = models.GenericIPAddressField(null=True)
    last_active = models.DateTimeField(default=timezone.now)




class AdminUserSessionsData(models.Model):
    uid = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    session_string = models.CharField(max_length=256, null=False)
    session_delete_string = models.CharField(max_length=256, null=False)
    session_create_time = models.DateTimeField(default=timezone.now)
    session_exp_time = models.DateTimeField(default=timezone.now)
    session_telemetry = models.ForeignKey(AdminSessionTelemetry, on_delete=models.CASCADE, null=True)

