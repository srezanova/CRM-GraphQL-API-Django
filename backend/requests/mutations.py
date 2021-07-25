import graphene
from graphql import GraphQLError
import requests

from .models import Request, Customer
from .schema import RequestType, CustomerType, StatusEnum, CategoryEnum
from users.models import User


class RequestInput(graphene.InputObjectType):
    '''
    Arguments for Request mutation classes.
    Defines fields allowing user to create or update the data.
    '''
    id = graphene.ID()
    description = graphene.String()
    customer_phone = graphene.String()
    category = CategoryEnum()
    status = StatusEnum()


class CustomerInput(graphene.InputObjectType):
    '''
    Arguments for Customer mutation classes.
    Defines fields allowing user to create or update the data.
    '''
    id = graphene.ID()
    phone = graphene.String(required=True)
    name = graphene.String()


class CreateRequest(graphene.Mutation):
    '''Creates a request. Employee is the user creating request.'''
    request = graphene.Field(RequestType)

    class Arguments:
        request_data = RequestInput(required=True)

    def mutate(self, info, request_data):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        try:
            customer = Customer.objects.get(phone=request_data.customer_phone)
        except Customer.DoesNotExist:
            customer = Customer(phone=request_data.customer_phone)
            customer.save()

        request = Request(
            description=request_data.description,
            customer=customer,
            employee=user,
            category=request_data.category,
            status=request_data.status,
        )

        request.save()
        return CreateRequest(request=request)


class UpdateRequest(graphene.Mutation):
    '''Update request by ID.'''
    request = graphene.Field(RequestType)

    class Arguments:
        request_data = RequestInput(required=True)

    def mutate(self, info, request_data):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        request_instance = Request.objects.get(
            id=request_data.id)

        if request_data.description is not None:
            request_instance.description = request_data.description
        if request_data.category is not None:
            request_instance.category = request_data.category
        if request_data.status is not None:
            request_instance.status = request_data.status

        request_instance.save()

        return UpdateRequest(request=request_instance)


class DeleteRequest(graphene.Mutation):
    '''Delete request by ID.'''
    id = graphene.ID()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        request = Request.objects.get(id=id)

        if request is not None:
            request.delete()

        return DeleteRequest(id=id)


class CreateCustomer(graphene.Mutation):
    '''Creates a customer.'''
    customer = graphene.Field(CustomerType)

    class Arguments:
        customer_data = CustomerInput(required=True)

    def mutate(self, info, customer_data):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        customer = Customer(
            phone=customer_data.phone,
            name=customer_data.name,
        )

        customer.save()
        return CreateCustomer(customer=customer)


class UpdateCustomer(graphene.Mutation):
    '''Updates a customer with customerPhone.'''
    customer = graphene.Field(CustomerType)

    class Arguments:
        customer_data = CustomerInput(required=True)

    def mutate(self, info, customer_data):

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        customer = Customer.objects.get(phone=customer_data.phone)
        if customer_data.name is not None:
            customer.name = customer_data.name

        customer.save()
        return UpdateCustomer(customer=customer)


class DeleteCustomer(graphene.Mutation):
    '''Deletes a customer with customerPhone.'''
    phone = graphene.String()

    class Arguments:
        phone = graphene.String(required=True)

    def mutate(self, info, phone):

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        customer = Customer.objects.get(phone=phone)
        if customer is not None:
            customer.delete()

        return DeleteCustomer(phone=phone)


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    create_request = CreateRequest.Field()
    update_customer = UpdateCustomer.Field()
    update_request = UpdateRequest.Field()
    delete_customer = DeleteCustomer.Field()
    delete_request = DeleteRequest.Field()
