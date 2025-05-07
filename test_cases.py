import unittest
from unittest.mock import patch
from io import StringIO
import main

class TestMain(unittest.TestCase):

##############################
# breakdown_keyword(user_input) -> str|None
##############################
    def test_breakdown_keyword(self):
        self.assertEqual(main.breakdown_keyword(''), None)
        
    def test_breakdown_keyword_2(self):
        self.assertEqual(main.breakdown_keyword("add \"task\""), "add")

    def test_breakdown_keyword_3(self):
        self.assertEqual(main.breakdown_keyword("update 1 'new task'"), "update")

    def test_breakdown_keyword_4(self):
        self.assertEqual(main.breakdown_keyword("delete 1"), "delete")
    
##############################
# breakdown_idx(user_input) -> int|None
##############################
    def test_breakdown_idx(self):
        self.assertEqual(main.breakdown_idx(''), None)
        
    def test_breakdown_idx_2(self):
        self.assertEqual(main.breakdown_idx("add \"task\""), None)

    def test_breakdown_idx_3(self):
        self.assertEqual(main.breakdown_idx("update 1 \"new task\""), 1)

    def test_breakdown_idx_4(self):
        self.assertEqual(main.breakdown_idx("delete 1"), 1)

##############################
# breakdown_idx(user_input) -> int|None
##############################
    def test_breakdown_description(self):
        self.assertEqual(main.breakdown_description(''), None)
        
    def test_breakdown_description_2(self):
        self.assertEqual(main.breakdown_description("add \"task\""), "task")

    def test_breakdown_description_3(self):
        self.assertEqual(main.breakdown_description("update 1 \"new task\""), "new task")

    def test_breakdown_description_4(self):
        self.assertEqual(main.breakdown_description("delete 1"), None)

if __name__ == "__main__":
    unittest.main()