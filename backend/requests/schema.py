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
    REPLACEMENT = 'REPLACEMENT'
    RETURN = 'RETURN'


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
        RequestType, request_id=graphene.ID(required=True))
    request_by_customer = graphene.List(
        RequestType, customer_phone=graphene.ID(required=True))

    # customer queries
    all_customers = graphene.List(CustomerType)
    customer_by_id = graphene.Field(
        CustomerType, customer_id=graphene.ID(required=True))
    customer_by_phone = graphene.Field(
        CustomerType, customer_phone=graphene.String(required=True))

    # all_requests_filter_status_and_category = graphene.List(
    #     RequestType, status=StatusEnum(), category=CategoryEnum())
    # my_requests_filter_status_and_category = graphene.List(
    #     RequestType, status=StatusEnum(), category=CategoryEnum())
    # all_requests_filter_status_or_category = graphene.List(
    #     RequestType, status=StatusEnum(), category=CategoryEnum())
    # my_requests_filter_status_or_category = graphene.List(
    #     RequestType, status=StatusEnum(), category=CategoryEnum())
    # all_requests_filter_date = graphene.List(RequestType, date=graphene.String(
    # ), date_start=graphene.String(), date_end=graphene.String())
    # my_requests_filter_date = graphene.List(RequestType, date=graphene.String(
    # ), date_start=graphene.String(), date_end=graphene.String())

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

    def resolve_request_by_id(self, info, request_id):
        '''Resolves request by ID.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        return Request.objects.get(id=request_id)

    def resolve_request_by_customer(self, info, customer_phone):
        '''Resolves requests by customer phone.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        customer = Customer.objects.get(phone=customer_phone)

        return gql_optimizer.query(Request.objects.filter(customer=customer), info)

    def resolve_all_customer(self, info, **kwargs):
        '''Resolves all customers.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        return gql_optimizer.query(Customer.objects.all(), info)

    def resolve_customer_by_id(self, info, customer_id):
        '''Resolves customer by id.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        return Customer.objects.get(id=customer_id)

    def resolve_customer_by_id(self, info, customer_phone):
        '''Resolves customer by id.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        return Customer.objects.get(phone=customer_phone)

    # def resolve_all_requests_filter_status_and_category(self, info, status=None, category=None):
    #     '''
    #     Resolves all requests by status and category at the same time.
    #     '''
    #     user = info.context.user

    #     if user.is_anonymous:
    #         raise GraphQLError('You need to be logged in.')
    #     if user.is_staff:
    #         return gql_optimizer.query(Request.objects.filter((Q(status=status) & Q(category=category))), info)
    #     else:
    #         raise GraphQLError('Not found.')

    # def resolve_my_requests_filter_status_and_category(self, info, status=None, category=None):
    #     '''
    #     Resolves user's own requests by status and category at the same time.
    #     '''
    #     user = info.context.user

    #     if user.is_anonymous:
    #         raise GraphQLError('You need to be logged in.')
    #     if user.is_staff:
    #         return gql_optimizer.query(Request.objects.filter((Q(status=status) & Q(category=category) & Q(employee=user))), info)
    #     else:
    #         raise GraphQLError('Not found.')

    # def resolve_all_requests_filter_status_or_category(self, info, status=None, category=None):
    #     '''
    #     Resolves all requests by status or category
    #     '''
    #     user = info.context.user

    #     if user.is_anonymous:
    #         raise GraphQLError('You need to be logged in.')
    #     if user.is_staff:
    #         return gql_optimizer.query(Request.objects.filter(
    #             (Q(status=status) | Q(category=category))
    #         ), info)
    #     else:
    #         raise GraphQLError('Not found.')

    # def resolve_my_requests_filter_status_or_category(self, info, status=None, category=None):
    #     '''
    #     Resolves user's own requests by status and category at the same time.
    #     '''
    #     user = info.context.user

    #     if user.is_anonymous:
    #         raise GraphQLError('You need to be logged in.')
    #     if user.is_staff:
    #         return gql_optimizer.query(Request.objects.filter(
    #             ((Q(status=status) & Q(employee=user)) |
    #              (Q(category=category) & Q(employee=user)))
    #         ), info)
    #     else:
    #         raise GraphQLError('Not found.')

    # def resolve_all_requests_filter_date(self, info, date=None, date_start=None, date_end=None):
    #     '''
    #     Resolves all requests by date.
    #     '''
    #     user = info.context.user

    #     if user.is_anonymous:
    #         raise GraphQLError('You need to be logged in.')
    #     if user.is_staff:
    #         return gql_optimizer.query(Request.objects.filter(
    #             (Q(created_at=date) | Q(
    #                 created_at__range=[date_start, date_end]))
    #         ), info)
    #     else:
    #         raise GraphQLError('Not found.')

    # def resolve_my_requests_filter_date(self, info, date=None, date_start=None, date_end=None):
    #     '''
    #     Resolves all requests by date.
    #     '''
    #     user = info.context.user

    #     if user.is_anonymous:
    #         raise GraphQLError('You need to be logged in.')
    #     if user.is_staff:
    #         return gql_optimizer.query(Request.objects.filter(
    #             ((Q(created_at=date) & Q(employee=user)) | (
    #                 Q(created_at__range=[date_start, date_end]) & Q(employee=user)))
    #         ), info)
    #     else:
    #         raise GraphQLError('Not found.')
