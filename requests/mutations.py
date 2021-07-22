import graphene
from graphql import GraphQLError

from .models import Request
from .schema import RequestType
from users.models import User

class StatusEnum(graphene.Enum):
    OPEN = 'Open'
    SCHEDULED = 'Scheduled'
    CANCELED = 'Canceled'
    CLOSED = 'Closed'

class CategoryEnum(graphene.Enum):
    CONSULTING = 'Consulting'
    DIAGNOSIS = 'Diagnosis'
    REPAIR = 'Repair'
    REPLACEMENT = 'Replacement'
    RETURN = 'Return'
    COMPLAINT = 'Complaint'
    OTHER = 'Other'

class RequestInput(graphene.InputObjectType):
    '''
    Arguments for Request create/update mutation classes.
    Defines fields allowing user to create or change the data.
    '''
    request_id = graphene.ID()
    product = graphene.String()
    problem = graphene.String()
    solution = graphene.String()
    client_id = graphene.ID()
    employee_id = graphene.ID()
    category = CategoryEnum()
    status = StatusEnum()

class CreateRequest(graphene.Mutation):
    request = graphene.Field(RequestType)

    class Arguments:
        request_data = RequestInput(required=True)

    def mutate(self, info, request_data):
        # client = User.objects.get(id=request_data.client_id)
        # employee = User.objects.get(id=request_data.employee_id)
        request_instance = Request(
            product=request_data.product,
            problem=request_data.problem,
            solution=request_data.solution,
            client_id=request_data.client_id,
            employee_id=request_data.employee_id,
            category=request_data.category,
            status=request_data.status,
        )
        request_instance.save()
        return CreateRequest(request=request_instance)

class UpdateRequest(graphene.Mutation):
    request = graphene.Field(RequestType)

    class Arguments:
        request_data = RequestInput(required=True)

    def mutate(self, info, request_data):
        request_instance = Request.objects.get(id=request_data.request_id)
        if request_data.product is not None:
            request_instance.product = request_data.product
        if request_data.problem is not None:
            request_instance.problem = request_data.problem
        if request_data.solution is not None:
            request_instance.solution = request_data.solution
        if request_data.client_id is not None:
            request_instance.client_id = request_data.client_id
        if request_data.employee_id is not None:
            request_instance.employee_id = request_data.employee_id
        if request_data.category is not None:
            request_instance.category = request_data.category
        if request_data.status is not None:
            request_instance.status = request_data.status
        request_instance.save()
        return UpdateRequest(request=request_instance)

class DeleteRequest(graphene.Mutation):
    request = graphene.Field(RequestType)

    class Arguments:
        request_id = graphene.ID(required=True)

    def mutate(self, info, request_id):
        request_instance = Request.objects.get(id=request_id)
        request_instance.delete()
        return None

class Mutation(graphene.ObjectType):
    create_request = CreateRequest.Field()
    update_request = UpdateRequest.Field()
    delete_request = DeleteRequest.Field()