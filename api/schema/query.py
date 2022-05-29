from django.http import HttpRequest
import graphene

from api.models import Profile, Category, Waste, Income
from api.schema.nodes import ProfileNode, CategoryNode, WasteNode, IncomeNode



class Query(graphene.ObjectType):
    """Описание запросов и типов данных"""
    profile = graphene.List(ProfileNode)
    categories = graphene.List(CategoryNode)
    wastes = graphene.List(WasteNode)
    incomes = graphene.List(IncomeNode)

    def resolve_categories(self, info: HttpRequest):
        user = info.context.user
        return Category.objects.filter(profile__user=user)

    def resolve_profile(self, info: HttpRequest):
        user = info.context.user
        return Profile.objects.filter(user=user)

    def resolve_wastes(self, info: HttpRequest):
        user = info.context.user
        return Waste.objects.all(category__profile__user=user)

    def resolve_incomes(self, info: HttpRequest):
        user = info.context.user
        return Income.objects.all(category__profile__user=user)
