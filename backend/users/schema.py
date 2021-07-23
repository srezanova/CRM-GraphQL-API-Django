import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
import graphene_django_optimizer as gql_optimizer

from users.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ['password', 'requests']
        description = " Type definition for a single request "

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    me = graphene.Field(UserType, id=graphene.ID())

    def resolve_all_users(self, info, **kwargs):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        if user.is_superuser == False:
            raise GraphQLError('Access denied.')

        if user.is_superuser:
            return gql_optimizer.query(User.objects.all(), info)

    def resolve_user(self, info, id):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        if user.is_staff == False:
            raise GraphQLError('Access denied.')

        return User.objects.get(id=id)

    def resolve_me(self, info):
        user = info.context.user
        return user
