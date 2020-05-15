from django.db import models

from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing','Billing'),
    ('shipping','Shipping'),
)
PROVINCE_NUMBER = (
    ('province1','Province No. 1'),
    ('province2','Province No. 2'),
    ('province3','Province No. 3'),
    ('province4','Gandaki Pradesh'),
    ('province5','Province No. 5'),
    ('province6','Karnali Pradesh'),
    ('province7','Sudurpashchim Pradesh'),
)

class Address(models.Model):
    billing_profile  = models.ForeignKey(BillingProfile)
    fullname         = models.CharField(max_length=120)
    address_type     = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1   = models.CharField(max_length=120)
    address_line_2   = models.CharField(max_length=120, null=True, blank=True)
    province         = models.CharField(max_length=120, choices=PROVINCE_NUMBER)
    city             = models.CharField(max_length=120)
    phone_number     = models.BigIntegerField(null=False, blank=False)   

    def __str__(self):
        return str(self.billing_profile)