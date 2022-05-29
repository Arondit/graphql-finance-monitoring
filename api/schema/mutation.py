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

    def resolve_add_category(self, info: graphene.ResolveInfo, name: str, profile_id: int, limit: Optional[Decimal] = None):
        """Описание мутации добавления новой категории"""
        profile = Profile.objects.get(pk=profile_id, user=info.context.user)
        return Category.objects.create(profile=profile, name=name, limit=limit)

    def resolve_remove_category(self, info: graphene.ResolveInfo, category_id: int):
        """Мутация для удаления категории"""
        try:
            Category.objects.get(id=category_id, profile__user=info.context.user).delete()
        except Category.DoesNotExist:
            return False
        return True

    def resolve_set_limit(self, info: graphene.ResolveInfo, category_id: int, limit: Decimal):
        """Мутация, которая позволяет установить лимит расходов на категорию"""
        category = Category.objects.get(pk=category_id, profile__user=info.context.user)
        category.limit = limit 
        category.save()
        return category

    def resolve_set_category_name(self, info: graphene.ResolveInfo, category_id: int, name: str):
        """Мутация для изменения имени категории"""
        category = Category.objects.get(pk=category_id, profile__user=info.context.user)
        category.name = name 
        category.save()
        return category


class ProfileMutation:
    set_profile_name = graphene.Field(ProfileNode, profile_id=graphene.ID(), name=graphene.String(required=True))
    set_bill = graphene.Field(ProfileNode, profile_id=graphene.ID(), bill=graphene.Decimal(required=True))

    def resolve_set_profile_name(self, info: graphene.ResolveInfo, profile_id: int, name: str):
        profile = Profile.objects.get(pk=profile_id, user=info.context.user)
        profile.name = name 
        profile.save()
        return profile

    def resolve_set_bill(self, info: graphene.ResolveInfo, profile_id: int, bill: Decimal):
        profile = Profile.objects.get(pk=profile_id, user=info.context.user)
        profile.bill = bill 
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

    def resolve_add_waste(self, info: graphene.ResolveInfo, amount, name, category_id):
        category = Category.objects.get(pk=category_id, profile__user=info.context.user)
        return Waste.objects.create(category=category, name=name, amount=amount)
    
    def resolve_edit_waste(
        self, 
        info: graphene.ResolveInfo, 
        waste_id: int, 
        amount: Optional[Decimal] = None, 
        name: Optional[str] = None, 
        category_id: Optional[str] = None,
    ):
        waste = Waste.objects.get(pk=waste_id, category__profile__user=info.context.user)

        if amount is not None:
            waste.amount = amount
        if amount is not None:
            name.amount = name
        if category_id is not None:
            with suppress(Category.DoesNotExist):
                waste.category = Category.objects.get(pk=category_id)
        
        waste.save()
        return waste 

    def resolve_remove_waste(self, info: graphene.ResolveInfo, waste_id: int):
        try:
            Waste.objects.get(id=waste_id, category__profile__user=info.context.user).delete()
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

    def resolve_add_income(self, info: graphene.ResolveInfo, amount, name, category_id):
        category = Category.objects.get(pk=category_id, profile__user=info.context.user)
        return Income.objects.create(category=category, name=name, amount=amount)
    
    def resolve_edit_income(
        self, 
        info: graphene.ResolveInfo, 
        income_id: int, 
        amount: Optional[Decimal] = None, 
        name: Optional[str] = None, 
        category_id: Optional[str] = None,
    ):
        income = Income.objects.get(pk=income_id, category__profile__user=info.context.user)

        if amount is not None:
            income.amount = amount
        if amount is not None:
            name.amount = name
        if category_id is not None:
            with suppress(Category.DoesNotExist):
                income.category = Category.objects.get(pk=category_id)
        
        income.save()
        return income 

    def resolve_remove_income(self, info: graphene.ResolveInfo, income_id: int):
        try:
            Income.objects.get(id=income_id, category__profile__user=info.context.user).delete()
        except Income.DoesNotExist:
            return False
        return True

        
class Mutation(CategoryMutation, ProfileMutation, WasteMutation, IncomeMutation, graphene.ObjectType):
    """"""
