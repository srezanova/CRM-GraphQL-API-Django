import graphene
from graphql import GraphQLError

from .models import Request
from .schema import RequestType, StatusEnum, CategoryEnum
from users.models import User

class RequestInputEmployee(graphene.InputObjectType):
    '''
    Arguments for Request create/update mutation classes.
    Defines fields allowing user to create or change the data.
    '''
    request_id = graphene.ID()
    product = graphene.String()
    problem = graphene.String()
    solution = graphene.String()
    client_id = graphene.ID()
    category = CategoryEnum()
    status = StatusEnum()

class RequestInputClient(graphene.InputObjectType):
    '''
    Arguments for Request create/update mutation classes.
    Defines fields allowing user to create or change the data.
    '''
    product = graphene.String()
    problem = graphene.String()

class CreateRequest(graphene.Mutation):
    '''
    Staff can access all data in request.
    Client can only access product and problem.
    '''
    request = graphene.Field(RequestType)

    class Arguments:
        request_employee = RequestInputEmployee()
        request_client = RequestInputClient()

    def mutate(self, info, request_employee=None, request_client=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        if user.is_staff:
            request_instance = Request(
                product=request_employee.product,
                problem=request_employee.problem,
                solution=request_employee.solution,
                client_id=request_employee.client_id,
                employee=user,
                category=request_employee.category,
                status=request_employee.status,
            )
        if user.is_staff == False:
            request_instance = Request(
                product=request_client.product,
                problem=request_client.problem,
                client=user,
            )
        request_instance.save()
        return CreateRequest(request=request_instance)

class UpdateRequest(graphene.Mutation):
    '''
    Only staff can update requests.
    '''
    request = graphene.Field(RequestType)

    class Arguments:
        request_data = RequestInputEmployee(required=True)

    def mutate(self, info, request_data):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        if user.is_staff == False:
            raise GraphQLError('Access denied.')
        request_instance = Request.objects.get(id=request_data.request_id)
        if request_instance.employee == user or user.is_superuser:
            if request_data.product is not None:
                request_instance.product = request_data.product
            if request_data.problem is not None:
                request_instance.problem = request_data.problem
            if request_data.solution is not None:
                request_instance.solution = request_data.solution
            if request_data.client_id is not None:
                request_instance.client_id = request_data.client_id
            if request_data.category is not None:
                request_instance.category = request_data.category
            if request_data.status is not None:
                request_instance.status = request_data.status
            request_instance.save()
            return UpdateRequest(request=request_instance)

class DeleteRequest(graphene.Mutation):
    '''
    Only superuser can delete requests.
    '''
    request_id = graphene.ID()

    class Arguments:
        request_id = graphene.ID(required=True)

    def mutate(self, info, request_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        if user.is_superuser != True:
            raise GraphQLError('Access denied.')
        request = Request.objects.get(id=request_id)
        if request is not None:
            request.delete()
        return DeleteRequest(request_id=request_id)

class Mutation(graphene.ObjectType):
    create_request = CreateRequest.Field()
    update_request = UpdateRequest.Field()
    delete_request = DeleteRequest.Field()