from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from django.templatetags.static import static

import os

def path_and_rename(instance, filename):
    upload_to = 'uploads/'
    ext = filename.split('.')[-1]
    # 'beneficiary_reference_id', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'from_db', 'full_clean', 'full_name', 'get_deferred_fields', 'id', 'mobile_number', 'mobile_number_regex', 'objects', 'otp', 'otp_regex', 'pk', 'prepare_database_save', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'session_key', 'token', 'txnId', 'unique_error_message', 'user_photo', 'validate_unique']
    print(f">> instance.mobile_number: {instance.session_key}")
    filename = f"user_photo.{ext}"
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class UserDataModel(models.Model):
    mobile_number_regex = RegexValidator(regex=r'[0-9]{10}', message="Enter 10 digit Mobile Number without Country Code")
    otp_regex = RegexValidator(regex=r'[0-9]{6}')

    mobile_number = models.CharField(validators=[mobile_number_regex], max_length=10, blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    txnId = models.CharField(max_length=36, blank=True)
    otp = models.CharField(validators=[otp_regex], max_length=6, blank=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)
    token = models.CharField(max_length=500, blank=True)
    beneficiary_reference_id = models.CharField(max_length=500, blank=True)
    user_photo = models.ImageField(upload_to=path_and_rename, default=static('user_photo.png'), validators=[FileExtensionValidator(['jpg'])])

    def __str__(self):
        return self.mobile_number
