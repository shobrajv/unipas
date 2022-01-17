from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import HomePageView, GenerateUtpPassView, ConfirmOtpView, GeneratePassView, UserPhotoView

urlpatterns = [
    path("generate_utp_pass/", GenerateUtpPassView.as_view(), name="generate_utp_pass"),
    path("confirm_otp/", ConfirmOtpView.as_view(), name="confirm_otp"),
    path("upload_photo/", UserPhotoView.as_view(), name="user_photo"),
    path("generate_pass/", GeneratePassView.as_view(), name="generate_pass"),
    path("", HomePageView.as_view(), name="home"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
