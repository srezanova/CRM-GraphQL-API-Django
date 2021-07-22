import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
import graphene_django_optimizer as gql_optimizer

from .models import Request
from users.schema import UserType


class RequestType(DjangoObjectType):
    class Meta:
        model = Request
        exclude = ['requests']


class Query(graphene.ObjectType):
    all_requests = graphene.List(RequestType)
    request = graphene.Field(RequestType, id=graphene.ID())

    def resolve_all_requests(self, info, **kwargs):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        if user.is_superuser:
            return gql_optimizer.query(Request.objects.all(), info)
        elif user.is_staff:
            return gql_optimizer.query(Request.objects.filter(employee=info.context.user), info)
        elif user.is_staff == False:
            return gql_optimizer.query(Request.objects.filter(client=info.context.user), info)

    def resolve_request(self, info, id):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        request = Request.objects.get(id=id)

        if user.is_superuser:
            return request
        elif user == request.client or user == request.employee:
            return request
        else:
            raise GraphQLError('Not found')