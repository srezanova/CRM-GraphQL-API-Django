from django.test import TestCase
from unittest import skip

from requests.models import Request, Customer
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


class RequestModelTest(TestCase):
    def setUp(self):
        self.employee = User.objects.create_user(
            email='employee@test.com',
            password='testpassword',
        )

        self.customer = Customer.objects.create(
            phone='89170009900',
            name='Ann',
        )

        self.request = Request.objects.create(
            customer=self.customer,
            employee=self.employee,
            category='REPAIR',
            status='ACCEPTED',
            description='Broken screen',
        )

    def test_request_detail(self):
        self.assertEqual(self.request.customer, self.customer)
        self.assertEqual(self.request.customer.phone, '89170009900')
        self.assertEqual(self.request.customer.name, 'Ann')
        self.assertEqual(self.request.employee, self.employee)
        self.assertEqual(self.request.employee.email, 'employee@test.com')
        self.assertEqual(self.request.category, 'REPAIR')
        self.assertEqual(self.request.status, 'ACCEPTED')
        self.assertEqual(self.request.description, 'Broken screen')
