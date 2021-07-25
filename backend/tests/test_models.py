from django.test import TestCase
from unittest import skip

from tasks.models import Task, Customer
from users.models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com',
            password='testpassword',
        )

        self.superuser = User.objects.create_superuser(
            email='superuser@test.com',
            password='testpassword',
        )

    def tearDown(self):
        self.user.delete()
        self.superuser.delete()

    def test_user_detail(self):
        self.assertEqual(self.user.email, 'user@test.com')
        self.assertNotEqual(self.user.password,
                            'testpassword')  # hashed passwords
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)

    def test_superuser_detail(self):
        self.assertEqual(self.superuser.email, 'superuser@test.com')
        self.assertNotEqual(self.superuser.password,
                            'testpassword')  # hashed passwords
        self.assertTrue(self.superuser.is_superuser)
        self.assertTrue(self.superuser.is_staff)

    def test_user_no_email(self):
        with self.assertRaises(ValueError):
            user1 = User.objects.create_user(
                email='',
                password='testpassword',
            )

    def test_normalize_email(self):
        user3 = User.objects.create_user(
            email='   test1@TEST.COM   ',
            password='testpassword',
        )
        self.assertEqual(user3.email, 'test1@test.com')


class TaskModelTest(TestCase):
    def setUp(self):
        self.employee = User.objects.create_user(
            email='employee@test.com',
            password='testpassword',
        )

        self.customer = Customer.objects.create(
            phone='89170009900',
            name='Ann',
        )

        self.task = Task.objects.create(
            customer=self.customer,
            employee=self.employee,
            category='REPAIR',
            status='ACCEPTED',
            description='Broken screen',
        )

    def test_task_detail(self):
        self.assertEqual(self.task.customer, self.customer)
        self.assertEqual(self.task.customer.phone, '89170009900')
        self.assertEqual(self.task.customer.name, 'Ann')
        self.assertEqual(self.task.employee, self.employee)
        self.assertEqual(self.task.employee.email, 'employee@test.com')
        self.assertEqual(self.task.category, 'REPAIR')
        self.assertEqual(self.task.status, 'ACCEPTED')
        self.assertEqual(self.task.description, 'Broken screen')
