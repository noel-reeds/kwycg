import unittest
from unittest.mock import create_autospec, Mock
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
        self.userkeys = {'email':'', 'id':'', 'updated_at':'',
                            'username':'', 'created_at':'', 'passwd_hash':''}

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
        mock_to_dict = create_autospec(self.user.to_dict,
                                            return_value=self.userkeys)
        # invoke with fn with arguments, raises an error
        with self.assertRaises(TypeError):
            mock_to_dict(67)
        mock_to_dict()
        self.assertTrue(mock_to_dict.call_count > 0)
        mock_to_dict.assert_called_once_with()
        self.assertEqual(len(mock_to_dict()), 6)
        for key in self.userkeys:
            self.assertIn(key, mock_to_dict())
        self.assertIsInstance(mock_to_dict(), dict)

    def test_hash_passwd(self):
        """
        Test hash_passwd function to check that it hashes a
        password str to a hash.
        """
        mock_hash_passwd = create_autospec(self.user.hash_passwd, 
                                            return_value=None)
        # invoke with no arguments, raises an error
        with self.assertRaises(TypeError):
            mock_hash_passwd()
        # invoke with more that one positional arguments, raises an error
        with self.assertRaises(TypeError):
            mock_hash_passwd(67, 88)
        mock_hash_passwd(self.passwd)
        mock_hash_passwd.assert_called_once_with(self.passwd)
        self.assertTrue(hasattr(self.user, 'passwd_hash'))

    def test_verify_passwd(self):
        """
        Test verify_passwd method that it indeed returns
        a bool for True hash, otherwise False.
        """
        mock_verify_passwd = create_autospec(self.user.verify_passwd,
                        return_value=True)
        mock_verify_passwd(self.passwd)
        mock_verify_passwd.assert_called_once_with(self.passwd)
        # invoking the fn without args raises an error.
        with self.assertRaises(TypeError):
            mock_verify_passwd()
        # invoking an instance method with cls, raises an error.
        with self.assertRaises(TypeError):
            User.verify_passwd(self.passwd)
        # invoke fn with more than one positional argument, raises an error
        with self.assertRaises(TypeError):
            mock_verify_passwd(self.passwd, self.passwd)
        self.assertIsInstance(self.passwd, str)
        self.assertIsInstance(mock_verify_passwd(self.passwd), bool)
        self.assertTrue(mock_verify_passwd(self.passwd))

    def test_repr(self):
        """
        Test unofficial representation method for objects.
        """
        self.user.__repr__ = Mock(return_value='reeds - nre@y.me')
        self.user.__repr__()
        self.assertTrue(self.user.__repr__.called)
        self.user.__repr__.assert_called_once_with()
        self.assertTrue(self.user.__repr__.call_count > 0)
        self.assertIsInstance(self.user.__repr__(self.user), str)
        self.assertTrue(self.user.__repr__(self.user) == 'reeds - nre@y.me')
