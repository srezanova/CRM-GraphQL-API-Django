import graphene

import requests.schema
import requests.mutations

class Query(requests.schema.Query, graphene.ObjectType):
    pass

class Mutation(requests.mutations.Mutation):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
