from django.shortcuts import render
from rest_framework import viewsets,mixins

from authentication.models import CustomUser
from authentication.serializers import RegisterSerializer

# Create your views here.
class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer