""" """
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import ProfileSerializer
from project.authentication import APITokenAuthentication
from django.views.generic import View
from django.http import JsonResponse
from django.middleware import csrf
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import json
import re
from django.contrib.auth import authenticate
from project.celery_tasks import app

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, APITokenAuthentication]
    parser_classes = [JSONParser]

    def get_queryset(self):
        print("download profile")
        user = self.request.user
        results = get_user_model().objects.filter(pk=user.id)
        print(results)
        return results