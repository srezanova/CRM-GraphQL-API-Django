import graphene
from graphql import GraphQLError

from .models import Request, Customer
from .schema import RequestType, CustomerType, StatusEnum, CategoryEnum
from users.models import User


class RequestInput(graphene.InputObjectType):
    '''
    Arguments for Request mutation classes.
    Defines fields allowing user to create or update the data.
    '''
    request_id = graphene.ID()
    description = graphene.String()
    customer_phone = graphene.String()
    category = CategoryEnum()
    status = StatusEnum()


class CustomerInput(graphene.InputObjectType):
    '''
    Arguments for Customer mutation classes.
    Defines fields allowing user to create or update the data.
    '''
    customer_id = graphene.ID()
    phone = graphene.String(required=True)
    first_name = graphene.String()
    last_name = graphene.String()


class CreateRequest(graphene.Mutation):
    '''Creates a request. Employee is the user creating request.'''
    request = graphene.Field(RequestType)

    class Arguments:
        request_data = RequestInput(required=True)

    def mutate(self, info, request_data):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        customer = Customer.objects.get(phone=request_data.customer_phone)

        request = Request(
            description=request_data.description,
            customer=customer,
            employee=user,
            category=request_data.category,
            status=request_data.status,
        )

        request.save()
        return CreateRequest(request=request)


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
            first_name=customer_data.first_name,
            last_name=customer_data.last_name,
        )

        customer.save()
        return CreateCustomer(customer=customer)


class UpdateCustomer(graphene.Mutation):
    '''Updates a customer with customer_phone.'''
    customer = graphene.Field(CustomerType)

    class Arguments:
        customer_data = CustomerInput(required=True)

    def mutate(self, info, customer_data):

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        if customer_data.phone is not None:
            customer = Customer.objects.get(phone=customer_data.phone)
            if customer_data.first_name is not None:
                customer.first_name = customer_data.first_name
            if customer_data.last_name is not None:
                customer.last_name = customer_data.last_name
            else:
                raise GraphQLError('Cannot update without phone.')

        customer.save()
        return UpdateCustomer(customer=customer)

        # class UpdateRequest(graphene.Mutation):
        #     '''
        #     Only staff can update requests.
        #     '''
        #     request = graphene.Field(RequestType)

        #     class Arguments:
        #         request_data = RequestInput(required=True)

        #     def mutate(self, info, request_data):
        #         user = info.context.user
        #         if user.is_anonymous:
        #             raise GraphQLError('You need to be logged in.')
        #         if user.is_staff == False:
        #             raise GraphQLError('Access denied.')
        #         request_instance = Request.objects.get(id=request_data.request_id)
        #         if request_instance.employee == user or user.is_superuser:
        #             if request_data.product is not None:
        #                 request_instance.product = request_data.product
        #             if request_data.problem is not None:
        #                 request_instance.problem = request_data.problem
        #             if request_data.solution is not None:
        #                 request_instance.solution = request_data.solution
        #             if request_data.client_id is not None:
        #                 request_instance.client_id = request_data.client_id
        #             if request_data.category is not None:
        #                 request_instance.category = request_data.category
        #             if request_data.status is not None:
        #                 request_instance.status = request_data.status
        #             if request_data.contacts is not None:
        #                 request_instance.contacts = request_data.contacts
        #             if request_data.message is not None:
        #                 request_instance.message = request_data.message
        #             request_instance.save()
        #             return UpdateRequest(request=request_instance)

        # class DeleteRequest(graphene.Mutation):
        #     '''
        #     Only superuser can delete requests.
        #     '''
        #     request_id = graphene.ID()

        #     class Arguments:
        #         request_id = graphene.ID(required=True)

        #     def mutate(self, info, request_id):
        #         user = info.context.user
        #         if user.is_anonymous:
        #             raise GraphQLError('You need to be logged in.')
        #         if user.is_superuser != True:
        #             raise GraphQLError('Access denied.')
        #         request = Request.objects.get(id=request_id)
        #         if request is not None:
        #             request.delete()
        #         return DeleteRequest(request_id=request_id)


class Mutation(graphene.ObjectType):
    create_request = CreateRequest.Field()
    create_customer = CreateCustomer.Field()
    update_customer = UpdateCustomer.Field()
    # update_request = UpdateRequest.Field()
    # delete_request = DeleteRequest.Field()
