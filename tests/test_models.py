from django.test import TestCase
from django.db.utils import IntegrityError

from requests.models import Request
from users.models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.client = User.objects.create_user(
            email='client@test.com',
            password='testpassword',
            first_name='Tom',
            last_name='Smith',
            phone='+7(916)000-00-00',
        )

        self.staff = User.objects.create_staffuser(
            email='staff@test.com',
            password='testpassword',
            first_name='Ann',
            last_name='Richard',
            phone='+7(916)000-00-01',
        )

        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='testpassword',
            first_name='Chris',
            last_name='Bold',
            phone='+7(916)000-00-02',
        )

    def test_client_detail(self):
        self.assertEqual(self.client.email, 'client@test.com')
        self.assertNotEqual(self.client.password, 'testpassword') #hashed passwords
        self.assertEqual(self.client.first_name, 'Tom')
        self.assertEqual(self.client.last_name, 'Smith')
        self.assertEqual(self.client.phone, '+7(916)000-00-00')
        self.assertFalse(self.client.admin)
        self.assertFalse(self.client.staff)

    def test_staff_detail(self):
        self.assertEqual(self.staff.email, 'staff@test.com')
        self.assertNotEqual(self.staff.password, 'testpassword') #hashed passwords
        self.assertEqual(self.staff.first_name, 'Ann')
        self.assertEqual(self.staff.last_name, 'Richard')
        self.assertEqual(self.staff.phone, '+7(916)000-00-01')
        self.assertFalse(self.staff.admin)
        self.assertTrue(self.staff.staff)

    def test_admin_detail(self):
        self.assertEqual(self.admin.email, 'admin@test.com')
        self.assertNotEqual(self.admin.password, 'testpassword') #hashed passwords
        self.assertEqual(self.admin.first_name, 'Chris')
        self.assertEqual(self.admin.last_name, 'Bold')
        self.assertEqual(self.admin.phone, '+7(916)000-00-02')
        self.assertTrue(self.admin.admin)
        self.assertTrue(self.admin.staff)

    def test_user_no_email(self):
        with self.assertRaises(ValueError):
            user = User.objects.create_user(
                email='',
                password='testpassword',
                first_name='Jerry',
                last_name='Smith',
                phone='+7(916)000-00-03',
            )

    def test_duplicated_email(self):
        with self.assertRaises(IntegrityError):
            user = User.objects.create_user(
                email='client@test.com',
                password='testpassword',
                first_name='Gerald',
                last_name='Bolton',
                phone='+7(916)000-00-04',
            )

    def test_normalize_email(self):
        user = User.objects.create_user(
            email = '   test1@TEST.COM   ',
            password = 'testpassword',
            first_name='Monica',
            last_name='Bing',
            phone='+7(916)000-00-05',
        )
        self.assertEqual(user.email, 'test1@test.com')

class RequestModelTest(TestCase):
    def setUp(self):
        self.client = User.objects.create_user(
            email='client@test.com',
            password='testpassword',
            first_name='Tom',
            last_name='Smith',
            phone='+7(916)000-00-00',
        )

        self.staff = User.objects.create_staffuser(
            email='staff@test.com',
            password='testpassword',
            first_name='Ann',
            last_name='Richard',
            phone='+7(916)000-00-01',
        )

        self.request = Request.objects.create(
            client=self.client,
            employee=self.staff,
            product='Phone',
            category='Repair',
            status='Open',
            problem='Broken screen',
            solution='Fix screen',
        )

    def test_request_detail(self):
        self.assertEqual(self.request.client, self.client)
        self.assertEqual(self.request.employee, self.staff)
        self.assertEqual(self.request.product, 'Phone')
        self.assertEqual(self.request.category, 'Repair')
        self.assertEqual(self.request.status, 'Open')
        self.assertEqual(self.request.problem, 'Broken screen')
        self.assertEqual(self.request.solution, 'Fix screen')