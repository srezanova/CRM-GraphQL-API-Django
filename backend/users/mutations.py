import graphene
from graphql import GraphQLError

from users.schema import UserType
from users.models import User


class UpdateUser(graphene.Mutation):
    '''Changes user's email.'''
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String()

    def mutate(self, info, email):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        user_instance = User.objects.get(id=user.id)

        if user_instance != user:
            raise GraphQLError('Not found.')

        if email is not None:
            user_instance.email = email

        user_instance.save()

        return UpdateUser(user=user_instance)


class Mutation(graphene.ObjectType):
    update_user = UpdateUser.Field()
