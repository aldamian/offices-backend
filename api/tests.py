from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):

    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'testuser@super.com', 'testpassword', 'Admin', 'test', 'test',
            '', None, None, None, 0)
        self.assertEqual(str(super_user), 'testuser@super.com')
        self.assertEqual(super_user.role, 'Admin')
        self.assertEqual(super_user.desk_id, None)
        self.assertEqual(super_user.gender, '')
        self.assertEqual(super_user.birth_date, None)
        self.assertEqual(super_user.nationality, None)
        self.assertEqual(super_user.remote_percentage, 0)
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)