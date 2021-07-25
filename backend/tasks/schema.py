from django.db.models import Q
from django.test import client
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
import graphene_django_optimizer as gql_optimizer


from .models import Task, Customer
from users.schema import UserType


class StatusEnum(graphene.Enum):
    ACCEPTED = 'ACCEPTED'
    IN_PROGRESS = 'IN_PROGRESS'
    READY = 'READY'
    CLOSED = 'CLOSED'


class CategoryEnum(graphene.Enum):
    CONSULTING = 'CONSULTING'
    DIAGNOSIS = 'DIAGNOSIS'
    REPAIR = 'REPAIR'
    OTHER = 'OTHER'


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        description = "Type definition for a single task."

    created_at = graphene.String()


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        description = "Type definition for a single customer."


class Query(graphene.ObjectType):
    # task queries
    all_tasks = graphene.List(
        TaskType,
        customer_phone=graphene.String(),
        statuses=graphene.List(StatusEnum),
        category=CategoryEnum(),
        created_at=graphene.String(),
        date_start=graphene.String(),
        date_end=graphene.String()
    )
    task_by_id = graphene.Field(
        TaskType, id=graphene.ID(required=True))

    # customer queries
    all_customers = graphene.List(CustomerType)
    customer_by_id = graphene.Field(
        CustomerType, id=graphene.ID(required=True))

    def resolve_all_tasks(self, info, customer_phone=None, statuses=None, category=None, created_at=None, date_start=None, date_end=None):
        '''Resolves all tasks for any user.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        if customer_phone is not None:
            try:
                customer = Customer.objects.get(phone=customer_phone)
            except Customer.DoesNotExist:
                return []

        # saving passed args for filter and deleting fields we cannot pass in filter
        saved_args = locals()
        del saved_args['self']
        del saved_args['info']
        del saved_args['customer_phone']
        del saved_args['user']

        # creating new dict with not None args
        saved_args = {k: v for k, v in saved_args.items() if v is not None}

        # if no args were passed than return all tasks
        if len(saved_args) == 0:
            return gql_optimizer.query(Task.objects.all(), info)

        # if statuses were passed we replace them with new 'status__in' key
        if 'statuses' in saved_args.keys():
            statuses = list(set(saved_args['statuses']))
            del saved_args['statuses']
            saved_args['status__in'] = statuses

        # if date range was passed we filter them separately else return filter with passed args
        if 'date_start' in saved_args.keys():
            del saved_args['date_start']
            del saved_args['date_end']
            return gql_optimizer.query(Task.objects.filter(**saved_args).filter(created_at__range=[date_start, date_end]), info)

        else:
            return gql_optimizer.query(Task.objects.filter(**saved_args), info)

    def resolve_task_by_id(self, info, id):
        '''Resolves task by ID.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        try:
            return Task.objects.get(id=id)
        except Task.DoesNotExist:
            raise GraphQLError('Not found.')

    def resolve_all_customers(self, info, phone=None):
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

        try:
            return Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            raise GraphQLError('Not found.')
