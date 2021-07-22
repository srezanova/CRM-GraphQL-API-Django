import graphene
from django.contrib.auth import get_user_model

from graphene_django.types import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery, UserNode
from graphql_auth import mutations

import requests.schema
import requests.mutations
import users.mutations

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    login = mutations.ObtainJSONWebToken.Field()
    refresh_token = mutations.RefreshToken.Field()

class Query(UserQuery, MeQuery, requests.schema.Query, graphene.ObjectType):
    pass

class Mutation(
    AuthMutation,
    requests.mutations.Mutation,
    users.mutations.Mutation,
    ):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
