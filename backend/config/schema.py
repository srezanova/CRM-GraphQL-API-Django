import graphene
from graphql_auth import mutations

import requests.schema
import requests.mutations
import users.mutations
import users.schema


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    login = mutations.ObtainJSONWebToken.Field()


class Query(users.schema.Query, requests.schema.Query, graphene.ObjectType):
    pass


class Mutation(AuthMutation, users.mutations.Mutation, requests.mutations.Mutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
