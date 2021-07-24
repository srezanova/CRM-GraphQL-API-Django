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

        self.user2 = User.objects.create(
            id=101,
            email='user2@test.com',
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
            name='Frank',
        )

        self.request = Request.objects.create(
            id=300,
            employee=self.user,
            category='DIAGNOSIS',
            status='ACCEPTED',
            description='Broken phone.',
            customer=self.customer,
        )

        self.request1 = Request.objects.create(
            id=302,
            employee=self.user,
            category='DIAGNOSIS',
            status='CLOSED',
            description='Broken phone.',
            customer=self.customer,
        )

        self.request2 = Request.objects.create(
            id=301,
            employee=self.user2,
            category='CONSULTING',
            status='CLOSED',
            description='Broken phone.',
            customer=self.customer2,
        )

    def tearDown(self):
        self.user.delete()
        self.customer.delete()
        self.customer2.delete()
        self.request.delete()
        self.request1.delete()
        self.request2.delete()

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

    def test_customer_by_id_query(self):
        query = '''
            query {
                customerById(id:200) {
                    id
                    phone
                    name
                }
            }
                '''

        expected = {'customerById': {
            'id': '200',
            'phone': '+7(800)-000-00-00',
            'name': 'Jerry', }}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_customers_query(self):
        query = '''
            query {
                allCustomers {
                    id
                    phone
                    name
                }
            }
                '''

        expected = {'allCustomers': [
            {'id': '200', 'phone': '+7(800)-000-00-00',
             'name': 'Jerry'},
            {'id': '201', 'phone': '+7(801)-000-00-00',
             'name': 'Frank'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_requests_query(self):
        query = '''
            query {
                allRequests {
                    id
                    description
                    category
                    status
                }
            }
                '''

        expected = {'allRequests': [
            {'category': 'DIAGNOSIS', 'description': 'Broken phone.',
             'id': '300', 'status': 'ACCEPTED'},
            {'category': 'DIAGNOSIS', 'description': 'Broken phone.',
             'id': '302', 'status': 'CLOSED'},
            {'category': 'CONSULTING', 'description': 'Broken phone.',
             'id': '301',  'status': 'CLOSED'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_requests_query_filter_by_phone(self):
        query = '''
            query {
                allRequests (customerPhone:"+7(801)-000-00-00") {
                    customer {
                        phone
                    }
                    status
                    category
                }
            }
                '''

        expected = {'allRequests': [{'customer': {
            'phone': '+7(801)-000-00-00'},
            'status': 'CLOSED', 'category': 'CONSULTING'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_requests_query_filter_by_statuses1(self):
        query = '''
            query {
                allRequests (statuses:[ACCEPTED]) {
                    customer {
                        phone
                    }
                    status
                    category
                }
            }
                '''

        expected = {'allRequests': [{'customer': {
            'phone': '+7(800)-000-00-00'},
            'status': 'ACCEPTED', 'category': 'DIAGNOSIS'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_requests_query_filter_by_statuses2(self):
        query = '''
            query {
                allRequests (statuses:[ACCEPTED, CLOSED]) {
                    status
                    category
                }
            }
                '''

        expected = {'allRequests': [
            {'status': 'ACCEPTED', 'category': 'DIAGNOSIS'},
            {'status': 'CLOSED', 'category': 'DIAGNOSIS'},
            {'status': 'CLOSED', 'category': 'CONSULTING'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_requests_query_filter_by_category(self):
        query = '''
            query {
                allRequests (category:DIAGNOSIS) {
                    customer {
                        phone
                    }
                    status
                    category
                }
            }
                '''

        expected = {'allRequests': [
            {'customer': {'phone': '+7(800)-000-00-00'},
             'status': 'ACCEPTED', 'category': 'DIAGNOSIS'},
            {'customer': {'phone': '+7(800)-000-00-00'},
             'status': 'CLOSED', 'category': 'DIAGNOSIS'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_requests_query_filter_by_date(self):
        date = self.request2.created_at

        query = f'query {{ allRequests (createdAt:"{date}") {{ id status category }} }}'

        expected = {'allRequests': [
            {'category': 'DIAGNOSIS', 'id': '300', 'status': 'ACCEPTED'},
            {'category': 'DIAGNOSIS', 'id': '302', 'status': 'CLOSED'},
            {'category': 'CONSULTING', 'id': '301', 'status': 'CLOSED'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_requests_query_filter_by_date_range(self):
        date = self.request2.created_at

        query = f'query {{ allRequests (dateStart:"{date}", dateEnd:"{date}") {{ id status category }} }}'

        expected = {'allRequests': [
            {'category': 'DIAGNOSIS', 'id': '300', 'status': 'ACCEPTED'},
            {'category': 'DIAGNOSIS', 'id': '302', 'status': 'CLOSED'},
            {'category': 'CONSULTING', 'id': '301', 'status': 'CLOSED'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_requests_query_many_filters(self):
        query = '''
            query {
                allRequests (category:DIAGNOSIS, statuses:[CLOSED]) {
                    customer {
                        phone
                    }
                    status
                    category
                }
            }
                '''

        expected = {'allRequests': [
            {'customer': {'phone': '+7(800)-000-00-00'},
             'status': 'CLOSED', 'category': 'DIAGNOSIS'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_request_by_id_query(self):
        query = '''
            query {
                requestById(id:300) {
                    id
                    status
                    customer {
                        id
                    }
                    employee {
                        id
                    }
                }
            }
                '''

        expected = {'requestById': {'id': '300', 'status': 'ACCEPTED',
                                    'customer': {'id': '200'},
                                    'employee': {'id': '100'}}}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_requests_query_not_found(self):
        query = '''
            query {
                allRequests(customerPhone:"0") {
                    id
                }
            }
                '''

        expected = {'allRequests': []}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)
