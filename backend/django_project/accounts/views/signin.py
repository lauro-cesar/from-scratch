from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import AccountSerializer
from project.authentication import APITokenAuthentication
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.middleware import csrf
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import json
import re

from django.contrib.auth import authenticate

isValidEmail = re.compile(r"[\w\.-]+@[\w\.-]+(\.[\w]+)+")

User = get_user_model()


class SignIn(View):
    def get(self, request):
        return JsonResponse({"csrftoken": "%s" % csrf.get_token(request)}, status=200)

    def post(self, request):
        body = json.loads(request.body)

        fields = {
            "password": "Please, check password",
            "email": "Please, check email",
            "first_name": "Please, check first_name",
            "last_name": "Please, check last_name",
            "username": "Please, check username",
        }
        try:
            u = User.objects.create(**body)
            u.full_clean()
        except Exception as e:
            print(e.__repr__())
            if isinstance(e, (IntegrityError)):
                return JsonResponse({"message": "Please, check username"}, status=400)
            if isinstance(e, (ValidationError)):
                for k, v in e.error_dict.items():
                    if k in fields.keys():
                        return JsonResponse({"message": fields[k]}, status=400)

        return JsonResponse({"message": "Please, check somenthing"}, status=400)
