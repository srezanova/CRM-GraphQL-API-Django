from django.db.models import Q
from django.test import client
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
import graphene_django_optimizer as gql_optimizer

from .models import Request, Customer
from users.schema import UserType


class StatusEnum(graphene.Enum):
    ACCEPTED = 'ACCEPTED'
    IN_PROCCESS = 'IN_PROCCESS'
    READY = 'READY'
    CLOSED = 'CLOSED'


class CategoryEnum(graphene.Enum):
    CONSULTING = 'CONSULTING'
    DIAGNOSIS = 'DIAGNOSIS'
    REPAIR = 'REPAIR'
    OTHER = 'OTHER'


class RequestType(DjangoObjectType):
    class Meta:
        model = Request
        description = "Type definition for a single request."

    created_at = graphene.String()


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        description = "Type definition for a single customer."


class Query(graphene.ObjectType):
    # request queries
    my_requests = graphene.List(RequestType)
    all_requests = graphene.List(RequestType)
    request_by_id = graphene.Field(
        RequestType, id=graphene.ID(required=True))
    request_by_customer = graphene.List(
        RequestType, customer_phone=graphene.ID(required=True))

    # customer queries
    all_customers = graphene.List(CustomerType)
    customer_by_id = graphene.Field(
        CustomerType, id=graphene.ID(required=True))
    customer_by_phone = graphene.Field(
        CustomerType, phone=graphene.String(required=True))

    # filters
    requests_filter_category = graphene.List(
        RequestType, category=CategoryEnum())
    requests_filter_status = graphene.List(
        RequestType, status1=StatusEnum(), status2=StatusEnum(), status3=StatusEnum())
    requests_filter_date = graphene.List(
        RequestType, date=graphene.String(), date_start=graphene.String(), date_end=graphene.String())

    def resolve_my_requests(self, info, **kwargs):
        '''Resolves user's own requests.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        return gql_optimizer.query(Request.objects.filter(employee=user), info)

    def resolve_all_requests(self, info, **kwargs):
        '''Resolves all requests for any user.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        return gql_optimizer.query(Request.objects.all(), info)

    def resolve_request_by_id(self, info, id):
        '''Resolves request by ID.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        return Request.objects.get(id=id)

    def resolve_request_by_customer(self, info, customer_phone):
        '''Resolves requests by customer phone.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        customer = Customer.objects.get(phone=customer_phone)

        return gql_optimizer.query(Request.objects.filter(customer=customer), info)

    def resolve_all_customers(self, info, **kwargs):
        '''Resolves all customers.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        return gql_optimizer.query(Customer.objects.all(), info)

    def resolve_customer_by_id(self, info, id):
        '''Resolves customer by id.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        return Customer.objects.get(id=id)

    def resolve_customer_by_phone(self, info, phone):
        '''Resolves customer by phone.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        return Customer.objects.get(phone=phone)

    def resolve_requests_filter_category(self, info, category):
        '''Resolves requests filtered by category.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        return gql_optimizer.query(Request.objects.filter(category=category), info)

    def resolve_requests_filter_status(self, info, status1=None, status2=None, status3=None):
        '''Resolves requests by one status or more.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        return gql_optimizer.query(Request.objects.filter((Q(status=status1) | Q(status=status2) | Q(status=status3))), info)

    def resolve_requests_filter_date(self, info, date=None, date_start=None, date_end=None):
        '''Resolves all requests by date or date range.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        return gql_optimizer.query(Request.objects.filter(
            (Q(created_at=date) | Q(created_at__range=[date_start, date_end]))
        ), info)
