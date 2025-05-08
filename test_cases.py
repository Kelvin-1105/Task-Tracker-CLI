import unittest
from unittest.mock import patch
import task_tracker

class TestMain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.resource = task_tracker.read_from_file("tasks.json")
    
    @classmethod
    def tearDownClass(cls):
        task_tracker.write_to_file("tasks.json", cls.resource)

##############################
# breakdown_keyword(user_input) -> str|None
##############################
    def test_breakdown_keyword(self):
        self.assertEqual(task_tracker.breakdown_keyword(''), None)
        
    def test_breakdown_keyword_2(self):
        self.assertEqual(task_tracker.breakdown_keyword("add \"task\""), "add")

    def test_breakdown_keyword_3(self):
        self.assertEqual(task_tracker.breakdown_keyword("update 1 'new task'"), "update")

    def test_breakdown_keyword_4(self):
        self.assertEqual(task_tracker.breakdown_keyword("delete 1"), "delete")
    
##############################
# breakdown_idx(user_input) -> int|None
##############################
    def test_breakdown_idx(self):
        self.assertEqual(task_tracker.breakdown_idx(''), None)
        
    def test_breakdown_idx_2(self):
        self.assertEqual(task_tracker.breakdown_idx("add \"task\""), None)

    def test_breakdown_idx_3(self):
        self.assertEqual(task_tracker.breakdown_idx("update 1 \"new task\""), 1)

    def test_breakdown_idx_4(self):
        self.assertEqual(task_tracker.breakdown_idx("delete 1"), 1)

##############################
# breakdown_description(user_input) -> str|None
##############################
    def test_breakdown_description(self):
        self.assertEqual(task_tracker.breakdown_description(''), None)
        
    def test_breakdown_description_2(self):
        self.assertEqual(task_tracker.breakdown_description("add \"task\""), "task")

    def test_breakdown_description_3(self):
        self.assertEqual(task_tracker.breakdown_description("update 1 \"new task\""), "new task")

    def test_breakdown_description_4(self):
        self.assertEqual(task_tracker.breakdown_description("delete 1"), None)

##############################
# breakdown_input(user_input) -> list[str|None, int|None, str|None]
##############################
    def test_breakdown_input(self):
        self.assertEqual(task_tracker.breakdown_input("add \"Groceries\""), ('add', None, 'Groceries'))

    def test_breakdown_input_2(self):
        self.assertEqual(task_tracker.breakdown_input("update 1 \"new task\""), ('update', 1, 'new task'))
    
    def test_breakdown_input3(self):
        self.assertEqual(task_tracker.breakdown_input("delete 1"), ('delete', 1, None))
##############################
# def merge_tasks(file_tasks, new_task) -> list: 
##############################
    def test_merge_tasks(self):
        self.assertEqual(task_tracker.merge_tasks([], [1]), [[1]])
        
    def test_merge_tasks_2(self):
        self.assertEqual(task_tracker.merge_tasks(
            [
                {
                    "id": 1,
                    "description": "something",
                    "status": "todo",
                    "createdAt": "May 07 2025 14:09:01",
                    "updatedAt": "May 07 2025 14:09:01"
                    }
                ], {
                    "id": 2,
                    "description": "more",
                    "status": "todo",
                    "createdAt": "May 07 2025 14:10:32",
                    "updatedAt": "May 07 2025 14:10:32"
                }), 
            [
                {
                    "id": 1,
                    "description": "something",
                    "status": "todo",
                    "createdAt": "May 07 2025 14:09:01",
                    "updatedAt": "May 07 2025 14:09:01"
                    }, 
                {
                    "id": 2,
                    "description": "more",
                    "status": "todo",
                    "createdAt": "May 07 2025 14:10:32",
                    "updatedAt": "May 07 2025 14:10:32"
                } 
            ]  
                )

#############################
# def find_id(file) -> int: 
#############################
    @patch.object(task_tracker, 'read_from_file', return_value=[{'id': 1}, {'id': 2}, {'id': 3},{'id': 5},{'id': 7}])
    def test_find_id(self, mock_method): 
        self.assertEqual(task_tracker.find_id("tasks.json"), 7)

##############################
# def file_exists(file) -> bool:
##############################
    @patch("os.path.isfile")
    def test_file_exists(self, mock_file):
        mock_file.return_value = True
        self.assertTrue(task_tracker.file_exists("tasks.json"))
    
    @patch("os.path.isfile")
    def test_file_exists_2(self, mock_file):
        mock_file.return_value = False
        self.assertFalse(task_tracker.file_exists("tasks.json"))

##############################
# def file_empty(file) -> bool:
##############################
    @patch.object(task_tracker, 'file_empty', return_value = [])
    def test_file_empty(self, mock_file):
        self.assertFalse(task_tracker.file_empty('tasks.json'))

    @patch.object(task_tracker, 'file_empty', return_value = None)
    def test_file_empty_2(self, mock_file):
        self.assertFalse(task_tracker.file_empty('tasks.json'))   

    @patch.object(task_tracker, 'file_empty', return_value = [{'id':1}])
    def test_file_empty_3(self, mock_file):
        self.assertTrue(task_tracker.file_empty('tasks.json'))

##############################
# def is_empty(tasks) -> bool:
##############################
    def test_is_empty(self):
        self.assertTrue(task_tracker.is_empty([]))
    
    def test_is_empty_2(self):
        self.assertFalse(task_tracker.is_empty([{'id':1}]))

if __name__ == "__main__":
    unittest.main()