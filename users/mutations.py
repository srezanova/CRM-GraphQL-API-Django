import graphene
from graphql import GraphQLError

from requests.schema import UserType
from users.models import User

class UserInput(graphene.InputObjectType):
    '''
    Arguments for User update mutation class.
    Defines fields allowing user to change the data.
    '''
    user_id = graphene.ID(required=True)
    first_name = graphene.String()
    last_name = graphene.String()
    phone = graphene.String()

class UpdateUser(graphene.Mutation):
    '''
    Changes additional information about user.
    First name, last name, phone.
    '''
    user = graphene.Field(UserType)

    class Arguments:
        user_data = UserInput(required=True)

    def mutate(self, info, user_data):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        user_instance = User.objects.get(id=user_data.user_id)

        if user != user_instance and user.is_staff == False:
            raise GraphQLError('Not found.')

        if user_instance == user or user.is_staff:
            if user_data.first_name is not None:
                user_instance.first_name = user_data.first_name
            if user_data.last_name is not None:
                user_instance.last_name = user_data.last_name
            if user_data.phone is not None:
                user_instance.phone = user_data.phone
            user_instance.save()
            return UpdateUser(user=user_instance)


class Mutation(graphene.ObjectType):
    update_user = UpdateUser.Field()
