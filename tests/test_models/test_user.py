import unittest
from unittest.mock import create_autospec
from models import User

class test_user_models(unittest.TestCase):
    """
    Tests functionalities of the user models.
    """
    def setUp(self):
        """
        Factors out repetitive setup for tests.
        """
        self.user = User(name='reeds', email='nre@y.me')
        self.passwd = 'passwd'
        self.userkeys = {'email', 'id', 'updated_at',
                            'username', 'created_at', 'passwd_hash'}

    def test_class_attributes(self):
        """
        Checks class attributes of user model to conform
        with the database entities..
        """
        self.assertTrue(hasattr(self.user, '__tablename__'))

    def test_to_dict(self):
        """
        Test to_dict instance method to check if it returns
        a dictionary or otherwise.
        """
        self.assertEqual(len(self.user.to_dict()), 6)
        for key in self.userkeys:
            self.assertIn(key, self.user.to_dict())
        self.assertIsInstance(self.user.to_dict(), dict)

    def test_hash_passwd(self):
        """
        Test hash_passwd function to check that it hashes a
        password str to a hash.
        """
        self.user.hash_passwd(self.passwd)
        self.assertTrue(hasattr(self.user, 'passwd_hash'))
        self.assertIsNotNone(self.user.__dict__.get('passwd_hash'))

    def test_verify_passwd(self):
        """
        Test verify_passwd method that it indeed returns
        a bool for True hash, otherwise False.
        """
        mock_verify_passwd = create_autospec(self.user.verify_passwd,
                        return_value=None)
        mock_verify_passwd(self.passwd)
        mock_verify_passwd.assert_called_once_with(self.passwd)
        self.assertIsInstance(self.passwd, str)
        self.user.hash_passwd(self.passwd)
        self.assertIsInstance(self.user.verify_passwd(self.passwd), bool)
        self.assertTrue(self.user.verify_passwd(self.passwd))
        self.assertFalse(self.user.verify_passwd('random passwd'))

    def test_repr(self):
        """
        Test unofficial representation method for objects.
        """
        self.assertIsInstance(repr(self.user), str)
        self.assertTrue(repr(self.user) == 'reeds - nre@y.me')
        self.assertTrue(repr(User) == "<class 'models.user.User'>")
