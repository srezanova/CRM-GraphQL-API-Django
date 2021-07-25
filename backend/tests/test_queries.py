from django.test import RequestFactory, TestCase
from unittest import skip
from graphql import GraphQLError
from graphene.test import Client

from users.models import User
from tasks.models import Task, Customer
from config.schema import schema


TestCase.maxDiff = None


def execute_query(query, user=None, variable_values=None, **kwargs):
    """
    Returns the results of executing a graphQL query using the graphene test client.
    """
    task_factory = RequestFactory()
    context_value = task_factory.get('/graphql/')
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

        self.task = Task.objects.create(
            id=300,
            employee=self.user,
            category='DIAGNOSIS',
            status='ACCEPTED',
            description='Broken phone.',
            customer=self.customer,
        )

        self.task1 = Task.objects.create(
            id=302,
            employee=self.user,
            category='DIAGNOSIS',
            status='CLOSED',
            description='Broken phone.',
            customer=self.customer,
        )

        self.task2 = Task.objects.create(
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
        self.task.delete()
        self.task1.delete()
        self.task2.delete()

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

    def test_all_tasks_query(self):
        query = '''
            query {
                allTasks {
                    id
                    description
                    category
                    status
                }
            }
                '''

        expected = {'allTasks': [
            {'category': 'DIAGNOSIS', 'description': 'Broken phone.',
             'id': '300', 'status': 'ACCEPTED'},
            {'category': 'DIAGNOSIS', 'description': 'Broken phone.',
             'id': '302', 'status': 'CLOSED'},
            {'category': 'CONSULTING', 'description': 'Broken phone.',
             'id': '301',  'status': 'CLOSED'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_tasks_query_filter_by_phone(self):
        query = '''
            query {
                allTasks (customerPhone:"+7(801)-000-00-00") {
                    customer {
                        phone
                    }
                    status
                    category
                }
            }
                '''

        expected = {'allTasks': [{'customer': {
            'phone': '+7(801)-000-00-00'},
            'status': 'CLOSED', 'category': 'CONSULTING'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_tasks_query_filter_by_statuses1(self):
        query = '''
            query {
                allTasks (statuses:[ACCEPTED]) {
                    customer {
                        phone
                    }
                    status
                    category
                }
            }
                '''

        expected = {'allTasks': [{'customer': {
            'phone': '+7(800)-000-00-00'},
            'status': 'ACCEPTED', 'category': 'DIAGNOSIS'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_tasks_query_filter_by_statuses2(self):
        query = '''
            query {
                allTasks (statuses:[ACCEPTED, CLOSED]) {
                    status
                    category
                }
            }
                '''

        expected = {'allTasks': [
            {'status': 'ACCEPTED', 'category': 'DIAGNOSIS'},
            {'status': 'CLOSED', 'category': 'DIAGNOSIS'},
            {'status': 'CLOSED', 'category': 'CONSULTING'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_tasks_query_filter_by_category(self):
        query = '''
            query {
                allTasks (category:DIAGNOSIS) {
                    customer {
                        phone
                    }
                    status
                    category
                }
            }
                '''

        expected = {'allTasks': [
            {'customer': {'phone': '+7(800)-000-00-00'},
             'status': 'ACCEPTED', 'category': 'DIAGNOSIS'},
            {'customer': {'phone': '+7(800)-000-00-00'},
             'status': 'CLOSED', 'category': 'DIAGNOSIS'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_tasks_query_filter_by_date(self):
        date = self.task2.created_at

        query = f'query {{ allTasks (createdAt:"{date}") {{ id status category }} }}'

        expected = {'allTasks': [
            {'category': 'DIAGNOSIS', 'id': '300', 'status': 'ACCEPTED'},
            {'category': 'DIAGNOSIS', 'id': '302', 'status': 'CLOSED'},
            {'category': 'CONSULTING', 'id': '301', 'status': 'CLOSED'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_tasks_query_filter_by_date_range(self):
        date = self.task2.created_at

        query = f'query {{ allTasks (dateStart:"{date}", dateEnd:"{date}") {{ id status category }} }}'

        expected = {'allTasks': [
            {'category': 'DIAGNOSIS', 'id': '300', 'status': 'ACCEPTED'},
            {'category': 'DIAGNOSIS', 'id': '302', 'status': 'CLOSED'},
            {'category': 'CONSULTING', 'id': '301', 'status': 'CLOSED'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_tasks_query_many_filters(self):
        query = '''
            query {
                allTasks (category:DIAGNOSIS, statuses:[CLOSED]) {
                    customer {
                        phone
                    }
                    status
                    category
                }
            }
                '''

        expected = {'allTasks': [
            {'customer': {'phone': '+7(800)-000-00-00'},
             'status': 'CLOSED', 'category': 'DIAGNOSIS'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_task_by_id_query(self):
        query = '''
            query {
                taskById(id:300) {
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

        expected = {'taskById': {'id': '300', 'status': 'ACCEPTED',
                                 'customer': {'id': '200'},
                                 'employee': {'id': '100'}}}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_all_tasks_query_not_found(self):
        query = '''
            query {
                allTasks(customerPhone:"0") {
                    id
                }
            }
                '''

        expected = {'allTasks': []}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)
