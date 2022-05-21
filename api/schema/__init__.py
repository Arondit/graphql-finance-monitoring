import graphene

from api.schema.query import Query
from api.schema.mutation import Mutation

schema = graphene.Schema(query=Query, mutation=Mutation)
