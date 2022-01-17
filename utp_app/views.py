import datetime

from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from .forms import GetOtpForm, ConfirmOtpForm, UploadPhotoForm

from utp_app.utils import generate_otp, confirm_otp, get_beneficiary_reference_id, generate_qr_code
from utp_app.models import UserDataModel

class HomePageView(TemplateView):
    template_name = "home.html"


class GenerateUtpPassView(TemplateView):
    form_class = GetOtpForm
    template_name = "get_otp_form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        request.session.flush()
        request.session.create()
        assert request.session.session_key
        request.session["datetime"] = str(datetime.datetime.now())
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(f">> Data entered: {data}")
            obj = UserDataModel()
            obj.session_key = request.session.session_key
            print(f">> Current session key: {obj.session_key}")
            txnId = generate_otp(data["mobile_number"], data["full_name"])
            if not txnId:
                return HttpResponse("Could not generate OTP, Please try after sometime.")
            obj.txnId = txnId
            obj.mobile_number = data["mobile_number"]
            obj.full_name = data["full_name"]
            obj.save()
            # form.save()
            return HttpResponseRedirect('/confirm_otp/')
        else:
            print(form.errors)
            return HttpResponse("Invalid Data Entered!")


class ConfirmOtpView(TemplateView):
    form_class = ConfirmOtpForm
    template_name = "confirm_otp_form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        obj = UserDataModel.objects.all().filter(session_key=request.session.session_key)[0]
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(f">> OTP entered: {data}")
            obj.otp = data["otp"]
            request.session['otp'] = data["otp"]
            request.session.modified = True
            obj.token = confirm_otp(data["otp"], obj.txnId)
            obj.beneficiary_reference_id = get_beneficiary_reference_id(obj.token)
            print(f">> beneficiary_reference_id : {obj.beneficiary_reference_id}")
            obj.save()
            # form.save()
            return HttpResponseRedirect('/upload_photo/')
        else:
            print(form.errors)
            return HttpResponse("Invalid Data Entered!")


class UserPhotoView(TemplateView):
    form_class = UploadPhotoForm
    template_name = "user_photo_form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        obj = UserDataModel.objects.all().filter(session_key=request.session.session_key)[0]
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            print(f">> upload data: {data}")
            obj.user_photo = data["user_photo"]
            obj.save()
            form.save()
            return HttpResponseRedirect('/generate_pass/')
        else:
            print(form.errors)
            return HttpResponse("Invalid Data Entered!")
    

class GeneratePassView(TemplateView):
    template_name = "generate_pass.html"

    def get(self, request, *args, **kwargs):
        obj = UserDataModel.objects.all().filter(session_key=request.session.session_key)[0]
        generate_qr_code(f"D:/UNI_PASS/unipass/utp_server/utp_app/static/passes/{obj.beneficiary_reference_id}.png", obj.beneficiary_reference_id)
        print(f">> obj upload data: {obj.user_photo}")
        print(f">> obj beneficiary_reference_id: {obj.beneficiary_reference_id}")

        from html2image import Html2Image
        hti = Html2Image()
        hti.output_path = "D:/UNI_PASS/unipass/utp_server/utp_app/static/passes/"
        user_pic = f"D:/UNI_PASS/unipass/utp_server/media/{obj.user_photo}"
        qr_pic = f"D:/UNI_PASS/unipass/utp_server/media/uploads/{obj.beneficiary_reference_id}_qr.png"
        print(f">> qr_pic: {qr_pic}")

        html = f'<div style="position:absolute;width:480px;height:100px;top:0px;left:0px;"> \
                    <div style="position:absolute;width:480px;height:100px;top:10px;left:10px;background-color:yellow;border-style: solid;  border-width: thin;"> \
                        <p style="font-family:Helvetica;font-weight:bold;position:absolute;left:10px;top:5px;color:black;font-size:42px;">Universal Pass</p> \
                        <img id="" src="D:/UNI_PASS/unipass/utp_server/utp_app/static/karnataka_govt_logo.svg" alt="logo_govt_of_karnataka" style="position:absolute;width:80px; top: 20px;left:390px;"></img> \
                    </div> \
                    <div style="position:absolute;width:480px;height:100px;top:110px;left:10px;background-color:red;border-style: solid;  border-width: thin;"> \
                        <p style="position:absolute;left:10px;top:14px;color:white;font-size:16px;width:300px;line-height:20px;">The Ministry of Health and Family Welfare</p> \
                        <p style="position:absolute;right:10px;top:5px;color:white;font-size:16px;width:160px;text-align:center;">GOVERNMENT OF</p> \
                        <p style="position:absolute;right:10px;top:18px;color:white;font-size:26px;width:160px;text-align:center;">KARNATAKA</p> \
                    </div> \
                    <div style="position:absolute;width:480px;height:500px;top:190px;left:10px;background-color:#eeeeee;border-style: solid;  border-width: thin;"> \
                        <p style="position:absolute;font-weight:bold;left:20px;top:5px;color:black;font-size:16px;">{obj.full_name}</p> \
                        <p style="font-family:Helvetica;position:absolute;font-weight:bold;left:350px;top:5px;color:black;font-size:16px;">Class 3 Pass</p> \
                        <p style="position:absolute;font-weight:bold;left:20px;top:45px;color:black;font-size:16px;">MALE, 30</p> \
                        <p style="position:absolute;font-weight:bold;left:20px;top:100px;color:black;font-size:16px;">Beneficiary Reference ID:</p> \
                        <p style="position:absolute;font-weight:bold;left:20px;top:120px;color:black;font-size:16px;">{obj.beneficiary_reference_id}</p> \
                        <p style="position:absolute;font-weight:bold;left:20px;top:150px;color:black;font-size:16px;">FULLY VACCINATED</p> \
                        <p style="position:absolute;font-weight:bold;left:20px;top:180px;color:black;font-size:16px;">Dose 1:</p> \
                        <p style="position:absolute;font-weight:bold;left:20px;top:200px;color:black;font-size:16px;">27-06-2021</p> \
                        <p style="position:absolute;font-weight:bold;left:20px;top:240px;color:black;font-size:16px;">Dose 2:</p> \
                        <p style="position:absolute;font-weight:bold;left:20px;top:260px;color:black;font-size:16px;">27-06-2021</p> \
                        <p style="position:absolute;left:20px;top:480px;color:black;font-size:10px;">*Sample design created by ADGC for Karnataka Government Demo</p> \
                        <img id="" src={user_pic} alt="user_photo" style="position:absolute;width: 180px; top: 50px; left:280px;"></img> \
                        <img id="" src="D:/UNI_PASS/unipass/utp_server/utp_app/static/vaccination_source.png" alt="vaccination_source" style="position:absolute;width: 180px; top: 260px; left:280px;"></img> \
                        <img id="" src={qr_pic} alt="beneficiary_qr"  style="position:absolute;width: 180px; top: 300px; left: 20px;"></img> \
                    </div> \
                </div>'
        hti.screenshot(html_str=html, save_as=f"{obj.beneficiary_reference_id}.png", size=(500, 700))
        hti.screenshot(html_str=html, save_as=f"{obj.beneficiary_reference_id}.png", size=(500, 700))

        return render(request, self.template_name, {'beneficiary_id': f"{obj.beneficiary_reference_id}"})
