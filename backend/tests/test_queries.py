from django.test import RequestFactory, TestCase
from unittest import skip
from graphql import GraphQLError
from graphene.test import Client

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


class QueryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=100,
            email='user@test.com',
            password='testpassword',
        )

    def tearDown(self):
        self.user.delete()

    def test_me_query(self):
        query = '''
                query {
                    me {
                        id
                        email
                    }
                }
                '''

        expected = {'me': {
            'id': '100',
            'email': 'user@test.com',
        }}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    @skip('test')
    def test_request_query(self):
        query = '''
                query {
                    request (id:104) {
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
                                'id': '104',
                                'problem': 'Broken screen',
                                'product': 'Phone',
                                'solution': 'Fix screen',
                                'status': 'OPEN'}
                    }

        executed = execute_query(query, self.superuser)
        data = executed.get('data')
        self.assertEqual(data, expected)

    @skip('test')
    def test_all_requests_query(self):
        query = '''
                query {
                    allRequests {
                        id
                        status
                        category
                    }
                }
                '''

        expected = {'allRequests': [
            {'id': '104', 'status': 'OPEN', 'category': 'REPAIR'},
            {'id': '105', 'status': 'CANCELED', 'category': 'CONSULTING'}
        ]}

        executed = execute_query(query, self.superuser)
        data = executed.get('data')
        self.assertEqual(data, expected)

    @skip('test')
    def test_all_requests_filter_status_and_category(self):
        query = '''
                query {
                    allRequestsFilterStatusAndCategory (status:OPEN, category:REPAIR) {
                        id
                        status
                        category
                    }
                }
                '''

        expected = {'allRequestsFilterStatusAndCategory': [
            {'id': '104', 'status': 'OPEN', 'category': 'REPAIR'}]}

        executed = execute_query(query, self.staff2)
        data = executed.get('data')
        self.assertEqual(data, expected)

    @skip('test')
    def test_my_requests_filter_status_and_category(self):
        query = '''
                query {
                    myRequestsFilterStatusAndCategory (status:CANCELED, category:CONSULTING) {
                        id
                        status
                        category
                    }
                }
                '''

        expected = {'myRequestsFilterStatusAndCategory': [
            {'id': '105', 'status': 'CANCELED', 'category': 'CONSULTING'}]}

        executed = execute_query(query, self.staff2)
        data = executed.get('data')
        self.assertEqual(data, expected)

    @skip('test')
    def test_all_requests_filter_status_or_category(self):
        query = '''
                query {
                    allRequestsFilterStatusOrCategory (status:OPEN, category:CONSULTING) {
                        id
                        status
                        category
                    }
                }
                '''

        expected = {'allRequestsFilterStatusOrCategory': [
            {'id': '104', 'status': 'OPEN', 'category': 'REPAIR'},
            {'id': '105', 'status': 'CANCELED', 'category': 'CONSULTING'}
        ]}

        executed = execute_query(query, self.staff2)
        data = executed.get('data')
        self.assertEqual(data, expected)

    @skip('test')
    def test_my_requests_filter_status_or_category(self):
        query = '''
                query {
                    myRequestsFilterStatusOrCategory (status:OPEN, category:CONSULTING) {
                        id
                        status
                        category
                    }
                }
                '''

        expected = {'myRequestsFilterStatusOrCategory': [
            {'id': '105', 'status': 'CANCELED', 'category': 'CONSULTING'}]}

        executed = execute_query(query, self.staff2)
        data = executed.get('data')
        self.assertEqual(data, expected)

    @skip('test')
    def test_all_requests_filter_data(self):
        date = self.request1.created_at
        query = f'query {{ allRequestsFilterDate (date:"{date}") {{ id status category }} }}'

        expected = {'allRequestsFilterDate': [
            {'id': '104', 'status': 'OPEN', 'category': 'REPAIR'},
            {'id': '105', 'status': 'CANCELED', 'category': 'CONSULTING'}
        ]}

        executed = execute_query(query, self.staff2)
        data = executed.get('data')
        self.assertEqual(data, expected)

    @skip('test')
    def test_my_requests_filter_data(self):
        date = self.request1.created_at
        query = f'query {{ myRequestsFilterDate (date:"{date}") {{ id status category }} }}'

        expected = {'myRequestsFilterDate': [
            {'id': '105', 'status': 'CANCELED', 'category': 'CONSULTING'}]}

        executed = execute_query(query, self.staff2)
        data = executed.get('data')
        self.assertEqual(data, expected)
