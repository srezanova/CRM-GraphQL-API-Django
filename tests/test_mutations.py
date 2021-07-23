from django.test import RequestFactory, TestCase
from unittest import skip
from graphql import GraphQLError
from graphene.test import Client

from users.models import User
from requests.models import Request
from config.schema import schema

TestCase.maxDiff = None

def execute_test_client_api_query(query, user=None, variable_values=None, **kwargs):
    """
    Returns the results of executing a graphQL query using the graphene test client.  This is a helper method for our tests
    """
    request_factory = RequestFactory()
    context_value = request_factory.get('/graphql/')
    context_value.user = user
    client = Client(schema)
    executed = client.execute(query, context_value=context_value, variable_values=variable_values, **kwargs)
    return executed

class APITest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=100,
            email='user@test.com',
            password='testpassword',
            first_name='Tom',
            last_name='Smith',
            phone='+7(916)000-00-00',
        )

        self.user2 = User.objects.create(
            id=102,
            email='user2@test.com',
            password='testpassword',
            first_name='Jimmy',
            last_name='Craig',
            phone='+7(916)000-00-00',
        )

        self.staff = User.objects.create(
            id=101,
            email='staff@test.com',
            password='testpassword',
            first_name='Ann',
            last_name='Richard',
            phone='+7(916)000-00-01',
            is_staff=True,
        )

        self.superuser = User.objects.create(
            id=104,
            email='superuser@test.com',
            password='testpassword',
            is_superuser=True,
        )

        self.request1 = Request.objects.create(
            id=100,
            client=self.user,
            employee=self.staff,
            product='Phone',
            category='Repair',
            status='Open',
            problem='Broken screen',
            solution='Fix screen',
        )

    def tearDown(self):
        self.user.delete()
        self.user2.delete()
        self.staff.delete()
        self.superuser.delete()
        self.request1.delete()

    def test_me_query(self):
        query = '''
                query {
                    me {
                        id
                        email
                        firstName
                        lastName
                        phone
                    }
                }
                '''

        expected = {'me': {
                        'id':'100',
                        'email': 'user@test.com',
                        'firstName': 'Tom',
                        'lastName': 'Smith',
                        'phone': '+7(916)000-00-00'
                    }}

        executed = execute_test_client_api_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_user_query_by_staff(self):
        query = '''
            query {
                user(id:100) {
                    id
                    email
                    phone
                    isStaff
                    firstName
                    lastName
                }
            }
                '''

        expected = {'user': {
                        'id': '100',
                        'email': 'user@test.com',
                        'phone': '+7(916)000-00-00',
                        'isStaff': False,
                        'firstName': 'Tom',
                        'lastName': 'Smith'
                    }}

        executed = execute_test_client_api_query(query, self.staff)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_users_query(self):
        query = '''
                query {
                    allUsers {
                        id
                    }
                }
                '''

        expected = {'allUsers': [{'id': '100'}, {'id': '102'}, {'id': '101'}, {'id': '104'}]}

        executed = execute_test_client_api_query(query, self.superuser)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_request_query(self):
        query = '''
                query {
                    request (id:100) {
                        id
                        product
                        problem
                        solution
                        status
                        category
                        employee {
                            email
                        }
                        client {
                            email
                        }
                    }
                }
                '''

        expected = {'request': {'category': 'REPAIR',
                                'client': {'email': 'user@test.com'},
                                'employee': {'email': 'staff@test.com'},
                                'id': '100',
                                'problem': 'Broken screen',
                                'product': 'Phone',
                                'solution': 'Fix screen',
                                'status': 'OPEN'}
        }

        executed = execute_test_client_api_query(query, self.superuser)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_requests_query(self):
        query = '''
                query {
                    allRequests {
                        id
                        product
                        problem
                        solution
                        status
                        category
                        employee {
                            email
                        }
                        client {
                            email
                        }
                    }
                }
                '''

        expected = {'allRequests': [{'id': '100',
                                    'product': 'Phone',
                                    'problem': 'Broken screen',
                                    'solution': 'Fix screen',
                                    'status': 'OPEN',
                                    'category': 'REPAIR',
                                    'employee': {'email': 'staff@test.com'},
                                    'client': {'email': 'user@test.com'}}]
        }

        executed = execute_test_client_api_query(query, self.superuser)
        data = executed.get('data')
        self.assertEqual(data, expected)
