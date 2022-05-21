from django.http import HttpRequest
from graphene_django import DjangoObjectType

from api.models import Profile, Category, Waste, Income


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category


class WasteNode(DjangoObjectType):
    class Meta:
        model = Waste


class IncomeNode(DjangoObjectType):
    class Meta:
        model = Income
