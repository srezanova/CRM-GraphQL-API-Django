import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
import graphene_django_optimizer as gql_optimizer

from users.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ['id', 'email']
        description = "Type definition for a single user."


class Query(graphene.ObjectType):
    '''Resolves id and email of authenticated user.'''

    me = graphene.Field(UserType)

    def resolve_me(self, info):
        user = info.context.user
        return user
