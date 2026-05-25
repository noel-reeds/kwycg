import unittest
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
        self.ed = {'amount_spent', 'id', 'category', 'name',
                    'description', 'user_id', 'updated_at', 'created_at'}

    def test_str(self):
        """
        Test formal rep. of expense objects.
        """
        self.assertIsInstance(str(self.e), str)
        self.assertTrue(str(self.e), 'You spent KES.88 on tips.')

    def test_to_dict(self):
        self.assertTrue(self.e.to_dict(), dict)
        for k in self.ed:
            self.assertIn(k, self.e.to_dict()) 
