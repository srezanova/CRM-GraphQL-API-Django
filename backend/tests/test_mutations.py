from collections import OrderedDict
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

        self.customer = Customer.objects.create(
            id=200,
            phone='+7(800)-000-00-00',
            name='Jerry',
        )

        self.customer2 = Customer.objects.create(
            id=201,
            phone='+7(801)-000-00-00',
        )

        self.request = Request.objects.create(
            id=300,
            employee=self.user,
            category='DIAGNOSIS',
            status='ACCEPTED',
            description='Broken phone.',
            customer=self.customer,
        )

        self.request2 = Request.objects.create(
            id=301,
            employee=self.user1,
            category='CONSULTING',
            status='CLOSED',
            description='Broken phone.',
            customer=self.customer2,
        )

    def tearDown(self):
        self.user.delete()
        self.user1.delete()
        self.customer.delete()
        self.customer2.delete()
        self.request.delete()
        self.request2.delete()

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
            'register': {
                'success': True
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
            'login': {
                'success': True
            }
        }

        executed = execute_query(query, self.user1)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_create_request_mutation(self):
        query = '''
            mutation {
                createRequest (requestData:
                    {status:READY,
                    description:"Broken phone.",
                    customerPhone:"+7(800)-000-00-00",
                    category:REPAIR,
                    },
                    ) {
                        request{
                        customer {
                            phone
                        }
                        employee {
                            email
                        }
                        status
                        description
                        category
                        }
                }
                }
                '''

        expected = OrderedDict([('createRequest',
                                 {'request':
                                  {'customer': {'phone': '+7(800)-000-00-00'},
                                   'employee': {'email': 'user@test.com'},
                                      'status': 'READY',
                                      'description': 'Broken phone.',
                                      'category': 'REPAIR'}})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_create_customer_mutation(self):
        query = '''
            mutation {
                createCustomer(customerData:
                {phone:"+7(700)-000-00-00",
                name:"Chelsey"}) {
                    customer {
                        phone
                        name
                    }
                }
            }
                '''

        expected = OrderedDict([('createCustomer',
                                 {'customer': {'phone': '+7(700)-000-00-00',
                                               'name': 'Chelsey'}})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_update_customer_mutation(self):
        query = '''
            mutation {
                updateCustomer(customerData:
                {phone:"+7(801)-000-00-00",
                name:"Frank"}) {
                    customer {
                        phone
                        name
                    }
                }
            }
                '''

        expected = OrderedDict([('updateCustomer', {'customer': {
                               'phone': '+7(801)-000-00-00', 'name': 'Frank'}})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_delete_customer_mutation(self):
        query = '''
                mutation {
                    deleteCustomer(phone:"+7(801)-000-00-00") {
                        phone
                    }
                }
                '''

        expected = OrderedDict(
            [('deleteCustomer', {'phone': '+7(801)-000-00-00'})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_update_request_mutation(self):
        query = '''
            mutation {
                updateRequest(requestData:{
                    id:300,
                    status:ACCEPTED
                }) {
                    request {
                        description
                        category
                        status
                    }
                }
            }
                '''

        expected = OrderedDict([('updateRequest', {'request': {
                               'description': 'Broken phone.',
                               'category': 'DIAGNOSIS',
                               'status': 'ACCEPTED'}})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_delete_request_mutation(self):
        query = '''
                mutation {
                    deleteRequest(id:301) {
                        id
                    }
                }
                '''

        expected = OrderedDict([('deleteRequest', {'id': '301'})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)
