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
    executed = client.execute(
        query, context_value=context_value, variable_values=variable_values, **kwargs)
    return executed


class APITest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=100,
            email='user@test.com',
            password='testpassword',
            first_name='Tom',
            last_name='Smith',
            phone='+7(916)000-00-01',
        )

        self.user2 = User.objects.create(
            id=101,
            email='user2@test.com',
            password='testpassword',
            first_name='Jimmy',
            last_name='Craig',
            phone='+7(916)000-00-02',
        )

        self.staff = User.objects.create(
            id=102,
            email='staff@test.com',
            password='testpassword',
            first_name='Ann',
            last_name='Richard',
            phone='+7(916)000-00-03',
            is_staff=True,
        )

        self.staff2 = User.objects.create(
            id=106,
            email='staff2@test.com',
            password='testpassword',
            first_name='James',
            last_name='Bottom',
            phone='+7(916)000-00-04',
            is_staff=True,
        )

        self.superuser = User.objects.create(
            id=103,
            email='superuser@test.com',
            password='testpassword',
            is_superuser=True,
            is_staff=True,
        )

        self.request1 = Request.objects.create(
            id=104,
            client=self.user,
            employee=self.staff,
            product='Phone',
            category='Repair',
            status='Open',
            problem='Broken screen',
            solution='Fix screen',
        )

        self.request2 = Request.objects.create(
            id=105,
            client=self.user2,
            employee=self.staff2,
            product='Fridge',
            category='Consulting',
            status='Canceled',
            problem='Icecream is melting',
            solution='Unplugging it and plugging back fixed the problem',
        )

    def tearDown(self):
        self.user.delete()
        self.user2.delete()
        self.staff.delete()
        self.superuser.delete()
        self.request1.delete()
        self.request2.delete()

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
            'id': '100',
            'email': 'user@test.com',
            'firstName': 'Tom',
            'lastName': 'Smith',
                        'phone': '+7(916)000-00-01'
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
            'phone': '+7(916)000-00-01',
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

        expected = {'allUsers': [{'id': '100'}, {'id': '101'}, {
            'id': '102'}, {'id': '106'}, {'id': '103'}]}

        executed = execute_test_client_api_query(query, self.superuser)
        data = executed.get('data')
        self.assertEqual(data, expected)

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

        executed = execute_test_client_api_query(query, self.superuser)
        data = executed.get('data')
        self.assertEqual(data, expected)

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

        executed = execute_test_client_api_query(query, self.superuser)
        data = executed.get('data')
        self.assertEqual(data, expected)

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

        executed = execute_test_client_api_query(query, self.staff2)
        data = executed.get('data')
        self.assertEqual(data, expected)

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

        executed = execute_test_client_api_query(query, self.staff2)
        data = executed.get('data')
        self.assertEqual(data, expected)

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

        executed = execute_test_client_api_query(query, self.staff2)
        data = executed.get('data')
        self.assertEqual(data, expected)

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

        executed = execute_test_client_api_query(query, self.staff2)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_requests_filter_data(self):
        date = self.request1.created_at
        query = f'query {{ allRequestsFilterDate (date:"{date}") {{ id status category }} }}'

        expected = {'allRequestsFilterDate': [
            {'id': '104', 'status': 'OPEN', 'category': 'REPAIR'},
            {'id': '105', 'status': 'CANCELED', 'category': 'CONSULTING'}
        ]}

        executed = execute_test_client_api_query(query, self.staff2)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_my_requests_filter_data(self):
        date = self.request1.created_at
        query = f'query {{ myRequestsFilterDate (date:"{date}") {{ id status category }} }}'

        expected = {'myRequestsFilterDate': [
            {'id': '105', 'status': 'CANCELED', 'category': 'CONSULTING'}]}

        executed = execute_test_client_api_query(query, self.staff2)
        data = executed.get('data')
        self.assertEqual(data, expected)
