from contextlib import suppress
from decimal import Decimal
from typing import Optional
import graphene
from api.models import Category, Income, Profile, Waste

from api.schema.nodes import CategoryNode, IncomeNode, ProfileNode, WasteNode


class CategoryMutation:
    add_category = graphene.Field(
        CategoryNode,
        name=graphene.String(required=True),
        limit=graphene.Decimal(required=False),
        profile_id=graphene.Int(required=True),
    )
    remove_category = graphene.Field(graphene.Boolean, category_id=graphene.ID())
    set_limit = graphene.Field(CategoryNode, category_id=graphene.ID(), limit=graphene.Decimal(required=True))
    set_category_name = graphene.Field(CategoryNode, category_id=graphene.ID(), name=graphene.String(required=True))

    def resolve_add_category(self, info, name: str, profile_id: int, limit: Optional[Decimal] = None):
        profile = Profile.objects.get(pk=profile_id)
        return Category.objects.create(profile=profile, name=name, limit=limit)

    def resolve_remove_category(self, info, category_id: int):
        try:
            Category.objects.get(id=category_id).delete()
        except Category.DoesNotExist:
            return False
        return True

    def resolve_set_limit(self, info, category_id: int, limit: Decimal):
        category = Category.objects.get(pk=category_id)
        category.limit = limit 
        category.save()
        return category

    def resolve_set_category_name(self, info, category_id: int, name: str):
        category = Category.objects.get(pk=category_id)
        category.name = name 
        category.save()
        return category


class ProfileMutation:
    set_profile_name = graphene.Field(ProfileNode, profile_id=graphene.ID(), name=graphene.String(required=True))

    def resolve_set_profile_name(self, info, profile_id: int, name: str):
        profile = Profile.objects.get(pk=profile_id)
        profile.name = name 
        profile.save()
        return profile


class WasteMutation:
    add_waste = graphene.Field(
        WasteNode,
        amount=graphene.Decimal(required=True),
        name=graphene.String(required=True),
        category_id=graphene.Int(required=True),
    )
    edit_waste = graphene.Field(
        WasteNode,
        waste_id=graphene.Int(required=True),
        amount=graphene.Decimal(required=False),
        name=graphene.String(required=False),
        category_id=graphene.Int(required=False),
    )
    remove_waste = graphene.Field(graphene.Boolean, waste_id=graphene.ID(required=True))

    def resolve_add_waste(self, info, amount, name, category_id):
        category = Category.objects.get(pk=category_id)
        return Waste.objects.create(category=category, name=name, amount=amount)
    
    def resolve_edit_waste(
        self, 
        info, 
        waste_id: int, 
        amount: Optional[Decimal] = None, 
        name: Optional[str] = None, 
        category_id: Optional[str] = None,
    ):
        waste = Waste.objects.get(pk=waste_id)

        if amount is not None:
            waste.amount = amount
        if amount is not None:
            name.amount = name
        if category_id is not None:
            with suppress(Category.DoesNotExist):
                waste.category = Category.objects.get(pk=category_id)
        
        waste.save()
        return waste 

    def resolve_remove_waste(self, info, waste_id: int):
        try:
            Waste.objects.get(id=waste_id).delete()
        except Waste.DoesNotExist:
            return False
        return True


class IncomeMutation:
    add_income = graphene.Field(
        IncomeNode,
        amount=graphene.Decimal(required=True),
        name=graphene.String(required=True),
        category_id=graphene.Int(required=True),
    )
    edit_income = graphene.Field(
        WasteNode,
        income_id=graphene.Int(required=True),
        amount=graphene.Decimal(required=False),
        name=graphene.String(required=False),
        category_id=graphene.Int(required=False),
    )
    remove_income = graphene.Field(graphene.Boolean, income_id=graphene.ID(required=True))

    def resolve_add_income(self, info, amount, name, category_id):
        category = Category.objects.get(pk=category_id)
        return Income.objects.create(category=category, name=name, amount=amount)
    
    def resolve_edit_income(
        self, 
        info, 
        income_id: int, 
        amount: Optional[Decimal] = None, 
        name: Optional[str] = None, 
        category_id: Optional[str] = None,
    ):
        income = Income.objects.get(pk=income_id)

        if amount is not None:
            income.amount = amount
        if amount is not None:
            name.amount = name
        if category_id is not None:
            with suppress(Category.DoesNotExist):
                income.category = Category.objects.get(pk=category_id)
        
        income.save()
        return income 

    def resolve_remove_income(self, info, income_id: int):
        try:
            Income.objects.get(id=income_id).delete()
        except Income.DoesNotExist:
            return False
        return True

        
class Mutation(CategoryMutation, ProfileMutation, WasteMutation, IncomeMutation, graphene.ObjectType):
    """"""
