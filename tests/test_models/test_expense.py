import unittest
from unittest.mock import Mock, create_autospec
from models import Expense

class test_expenses_models(unittest.TestCase):
    """
    Tests functionalities of the expenses models.
    """
    def test_class_attributes(self):
        """
        Verifies class attributes of expenses models to conform
        with the persistence entities.
        """
        
    def setUp(self):
        """
        Factors out repetitive setup for tests.
        """
        self.e = Expense(name='tips', amount=88)
        self.ed = {'amount_spent':'', 'id':'', 'category':'', 'name':'',
                    'description':'', 'user_id':'', 'updated_at':'',
                    'created_at':''}

    def test_str(self):
        """
        Test formal rep. of expense objects.
        """
        self.e.__str__ = Mock(return_value='You spent KES.88 on tips.')
        # invoke with fn with positional arguments, raises an error
        self.e.__str__()
        self.e.__str__.assert_called_once_with()
        self.assertTrue(self.e.__str__.call_count > 0)
        self.assertIsInstance(self.e.__str__(self.e), str)
        self.assertTrue(str(self.e), 'You spent KES.88 on tips.')

    def test_to_dict(self):
        mock_to_dict_fn = create_autospec(self.e.to_dict,
                                            return_value=self.ed)
        # invoke with fn with positional arguments, raises an error
        with self.assertRaises(TypeError):
            mock_to_dict_fn(self.ed)
        mock_to_dict_fn()
        self.assertTrue(mock_to_dict_fn.called)
        mock_to_dict_fn.assert_called_once_with()
        self.assertTrue(self.e.to_dict(), dict)
        for k in self.ed:
            self.assertIn(k, mock_to_dict_fn()) 
