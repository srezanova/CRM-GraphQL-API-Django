from django.test import RequestFactory, TestCase
from unittest import skip
from graphql import GraphQLError
from graphene.test import Client
from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase

from users.models import User
from requests.models import Request, Customer
from config.schema import schema


TestCase.maxDiff = None


def execute_query(query, user=None, variable_values=None, **kwargs):
    """
    Returns the results of executing a graphQL query using the graphene test client.
    """
    request_factory = RequestFactory()
    context_value = request_factory.get('/graphql/')
    context_value.user = user
    client = Client(schema)
    executed = client.execute(
        query, context_value=context_value, variable_values=variable_values, **kwargs)
    return executed


class MutationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=100,
            email='user@test.com',
            password='testpassword',
        )

        self.user1 = User.objects.create_user(
            email='user1@test.com',
            password='testpassword',
        )

    def tearDown(self):
        self.user.delete()

    def test_update_user_mutation(self):
        query = '''
                mutation {
                    updateUser (email:"update_user@test.com") {
                        user {
                            id
                            email
                        }
                    }
                }
                '''

        expected = {'updateUser': {
            'user': {
                'id': '100',
                'email': 'update_user@test.com'
            }
        }}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_register_mutation(self):
        query = '''
            mutation {
                register (email:"test@test.com",
                    password1:"testpassword",
                    password2:"testpassword") {
                        success
                }
            }
                '''

        expected = {
            "register": {
                "success": True
            }
        }

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_login_mutation(self):
        query = '''
            mutation {
                login (email:"user1@test.com",
                password:"testpassword") {
                    success
                }
            }
                '''

        expected = {
            "login": {
                "success": True
            }
        }

        executed = execute_query(query, self.user1)
        data = executed.get('data')
        self.assertEqual(data, expected)
