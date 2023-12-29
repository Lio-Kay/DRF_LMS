import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework.views import APIView

UserModel = get_user_model()


class VerifyEmailAPIView(APIView):
    def get(self, request, key, *args, **kwargs):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/api/v1/dj-rest-auth/registration/verify-email/"
        redirect_url = settings.LOGIN_URL
        post_data = {'key': key}
        result = requests.post(post_url, data=post_data)
        return redirect(redirect_url)
