from django.db import models
from inception.s3_storage import gerber_storage
from database.models import User, Addresses
from datetime import datetime


# Create your models here.
def gerber_archive_path(instance, filename):
    return '{0}/{1}/archive/{2}'.format(instance.user_email, instance.date_time, filename)


def gerber_renders_path(instance, filename):
    return '{0}/{1}/renders/{2}'.format(instance.user_email, instance.date_time, filename)


def bills_path(instance, filename):
    return '{0}/{1}/bills/{2}'.format(instance.user_email, instance.date_time, filename)


def reports_path(instance, filename):
    return '{0}/{1}/reports/{2}'.format(instance.user_email, instance.date_time, filename)


def quatations_path(instance, filename):
    return '{0}/{1}/quatations/{2}'.format(instance.user_email, instance.date_time, filename)


class PCBMaterials(models.Model):
    value = models.CharField(max_length=20)
    price_weight = models.FloatField()
    is_available = models.BooleanField()
    quick_help_text = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = 'PCBMaterials'


class PCBCULayers(models.Model):
    value = models.IntegerField()
    price_weight = models.FloatField()
    is_available = models.BooleanField()
    quick_help_text = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = 'PCBCULayers'


class PCBThicknesses(models.Model):
    value = models.CharField(max_length=20)
    price_weight = models.FloatField()
    is_available = models.BooleanField()
    quick_help_text = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = 'PCBThicknesses'


class PCBCUThicknesses(models.Model):
    value = models.CharField(max_length=20)
    price_weight = models.FloatField()
    is_available = models.BooleanField()
    quick_help_text = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = 'PCBCUThicknesses'


class PCBSurfaceFinishes(models.Model):
    value = models.CharField(max_length=20)
    price_weight = models.FloatField()
    is_available = models.BooleanField()
    quick_help_text = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = 'PCBSurfaceFinishs'


class PCBColors(models.Model):
    value = models.CharField(max_length=20)
    price_weight = models.FloatField()
    is_available = models.BooleanField()
    quick_help_text = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = 'PCBColors'


class PCBSSColors(models.Model):
    value = models.CharField(max_length=20)
    price_weight = models.FloatField()
    is_available = models.BooleanField()
    quick_help_text = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = 'PCBSSColors'


class PCBOrderSettings(models.Model):
    pcb_width = models.IntegerField()
    pcb_length = models.IntegerField()
    pcb_material = models.ForeignKey(PCBMaterials, null=False, on_delete=models.CASCADE, default=None)
    pcb_copper_layers = models.ForeignKey(PCBCULayers, null=False, on_delete=models.CASCADE, default=None)
    pcb_copper_thickness = models.ForeignKey(PCBCUThicknesses, null=False, on_delete=models.CASCADE, default=None)
    pcb_thickness = models.ForeignKey(PCBThicknesses, null=False, on_delete=models.CASCADE, default=None)
    pcb_surface_finish = models.ForeignKey(PCBSurfaceFinishes, null=False, on_delete=models.CASCADE, default=None)
    pcb_color_top = models.ForeignKey(PCBColors, null=False, on_delete=models.CASCADE, default=None,
                                      related_name='pcb_color_top')
    pcb_color_bottom = models.ForeignKey(PCBColors, null=False, on_delete=models.CASCADE, default=None,
                                         related_name='pcb_color_bottom')
    pcb_slickscreen_color_top = models.ForeignKey(PCBSSColors, null=False, on_delete=models.CASCADE, default=None,
                                                  related_name='pcb_slickscreen_color_top')
    pcb_slickscreen_color_bottom = models.ForeignKey(PCBSSColors, null=False, on_delete=models.CASCADE, default=None,
                                                     related_name='pcb_slickscreen_color_bottom')

    class Meta:
        db_table = 'PCBOrderSettings'

    def clean(self):
        pass


class GerberFiles(models.Model):
    def init_order_params(self, email, order_id):
        self.user_email = email
        self.order_id = order_id
        self.date_time = '{:%Y-%m-%d-%H-%M-%S-%f}'.format(datetime.now())

    archive_file = models.FileField(storage=gerber_storage, null=False, blank=False, upload_to=gerber_archive_path)
    render_file = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_tc_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_bc_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_tsm_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_bsm_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_tss_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_bss_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic1_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic2_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic3_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic4_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic5_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic6_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic7_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic8_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic9_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic10_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic11_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic12_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic13_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic14_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic15_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic16_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic17_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic18_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic19_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic20_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic21_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic22_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic23_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic24_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic25_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic26_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic27_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic28_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic29_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic30_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic31_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_ic32_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_drill_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_non_plated_drill_layer = models.FileField(storage=gerber_storage, default=None,
                                                     upload_to=gerber_renders_path)
    render_edge_cut_layer = models.FileField(storage=gerber_storage, default=None, upload_to=gerber_renders_path)
    render_mechanical_outline_layer = models.FileField(storage=gerber_storage, default=None,
                                                       upload_to=gerber_renders_path)

    class Meta:
        db_table = 'GerberFiles'


class PCBOrders(models.Model):
    date_of_created = models.DateTimeField(default=datetime)
    date_of_updated = models.DateTimeField(default=datetime)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gerber_files = models.ForeignKey(GerberFiles, on_delete=models.CASCADE)
    pcb_settings = models.ForeignKey(PCBOrderSettings, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    order_type = models.CharField(max_length=10, null=True, default='0')
    shipping_address = models.ForeignKey(Addresses, null=True, on_delete=None)
    # billing_address=models.ForeignKey()
    transaction_uuid = models.UUIDField(unique=True)
    # payment_id=models.ImageField()
    is_lock = models.BooleanField(default=False)
    is_cost_calculated = models.BooleanField(default=False)
    base_amount = models.FloatField(null=True)
    discount_amount = models.FloatField(null=True)
    net_amount = models.FloatField(null=True)
    gst_amount = models.FloatField(null=True)
    total_amount = models.FloatField(null=True)
    is_paid = models.BooleanField(default=False)
    coupon_applied = models.CharField(null=True, blank=True, max_length=20)
    remarks = models.TextField(null=True)

    class Meta:
        db_table = 'PCBOrders'
