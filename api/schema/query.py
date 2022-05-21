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
        return Category.objects.all()

    def resolve_profile(self, info):
        return Profile.objects.all()

    def resolve_wastes(self, info):
        return Waste.objects.all()

    def resolve_incomes(self, info):
        return Income.objects.all()
