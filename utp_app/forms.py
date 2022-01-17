from django.forms import ModelForm
from utp_app.models import UserDataModel

class GetOtpForm(ModelForm):
    class Meta:
        model = UserDataModel
        fields = ['mobile_number', 'full_name']

class ConfirmOtpForm(ModelForm):
    class Meta:
        model = UserDataModel
        fields = ['otp']

class UploadPhotoForm(ModelForm):
    class Meta:
        model = UserDataModel
        fields = ['user_photo']
