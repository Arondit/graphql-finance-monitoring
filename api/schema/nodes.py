from django.http import HttpRequest
from graphene_django import DjangoObjectType

from api.models import Profile, Category, Waste, Income


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile

    @classmethod
    def get_queryset(cls, queryset, info: HttpRequest):
        user = info.context.user
        if user.is_authenticated:
            return queryset.filter(user=user)
        return queryset


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category

    @classmethod
    def get_queryset(cls, queryset, info: HttpRequest):
        user = info.context.user
        if user.is_authenticated:
            return queryset.filter(profile__user=user)
        return queryset


class WasteNode(DjangoObjectType):
    class Meta:
        model = Waste

    @classmethod
    def get_queryset(cls, queryset, info: HttpRequest):
        user = info.context.user
        if user.is_authenticated:
            return queryset.filter(category__profile__user=user)
        return queryset


class IncomeNode(DjangoObjectType):
    class Meta:
        model = Income

    @classmethod
    def get_queryset(cls, queryset, info: HttpRequest):
        user = info.context.user
        if user.is_authenticated:
            return queryset.filter(category__profile__user=user)
        return queryset
