import graphene

from api.models import Profile, Category, Waste, Income
from api.schema.nodes import ProfileNode, CategoryNode, WasteNode, IncomeNode



class Query(graphene.ObjectType):
    """Описание запросов и типов данных"""
    profile = graphene.List(ProfileNode)
    categories = graphene.List(CategoryNode)
    wastes = graphene.List(WasteNode)
    incomes = graphene.List(IncomeNode)

    def resolve_categories(self, info):
        user = info.context.user
        print(user)
        return Category.objects.filter(profile__user=user)

    def resolve_profile(self, info):
        user = info.context.user
        print(user)
        return Profile.objects.filter(user=user)

    def resolve_wastes(self, info):
        user = info.context.user
        print(user)
        return Waste.objects.all(category__profile__user=user)

    def resolve_incomes(self, info):
        user = info.context.user
        print(user)
        return Income.objects.all(category__profile__user=user)
