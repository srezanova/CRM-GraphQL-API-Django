import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
import graphene_django_optimizer as gql_optimizer

from .models import Request
from users.models import User



class UserType(DjangoObjectType):
    class Meta:
        model = User

class RequestType(DjangoObjectType):
    class Meta:
        model = Request

class Query(graphene.ObjectType):
    all_requests = graphene.List(RequestType)
    request = graphene.Field(RequestType, id=graphene.ID())

    def resolve_all_requests(self, info, **kwargs):
        return gql_optimizer.query(Request.objects.all(), info)

    def resolve_request(self, info, id):
        return Request.objects.get(id=id)
