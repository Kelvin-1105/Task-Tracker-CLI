import unittest
from unittest.mock import patch
import task_tracker

class TestMain(unittest.TestCase):

# Save .json contents 
    @classmethod
    def setUpClass(cls):
        cls.resource = task_tracker.read_from_file("tasks.json")

# Rewrite original .json contents 
    @classmethod
    def tearDownClass(cls):
        task_tracker.write_to_file("tasks.json", cls.resource)

##############################
# breakdown_keywords(user_input) -> str|None
##############################
    def test_breakdown_keyword(self):
        self.assertEqual(task_tracker.breakdown_keywords("1111111"), (None, None))

    def test_breakdown_keywords_2(self):
        self.assertEqual(task_tracker.breakdown_keywords("add \"task\""), ("add", None))

    def test_breakdown_keywords_3(self):
        self.assertEqual(task_tracker.breakdown_keywords("update 1 'new task'"), ("update", None))

    def test_breakdown_keywords_4(self):
        self.assertEqual(task_tracker.breakdown_keywords("delete 1"), ("delete", None))
    
    def test_breakdown_keywords_5(self):
        self.assertEqual(task_tracker.breakdown_keywords("list done"), ("list", 'done'))

    def test_breakdown_keywords_6(self):
        self.assertEqual(task_tracker.breakdown_keywords("list in-progress"), ("list", 'in-progress'))

    def test_breakdown_keywords_7(self):
        self.assertEqual(task_tracker.breakdown_keywords("mark in-progress 1"), ("mark", 'in-progress'))

##############################
# breakdown_idx(user_input) -> int|None
##############################
    def test_breakdown_idx_2(self):
        self.assertEqual(task_tracker.breakdown_idx("add \"task\""), None)

    def test_breakdown_idx_3(self):
        self.assertEqual(task_tracker.breakdown_idx("update 1 \"new task\""), 1)

    def test_breakdown_idx_4(self):
        self.assertEqual(task_tracker.breakdown_idx("delete 1"), 1)
    
    def test_breakdown_idx_5(self):
        self.assertEqual(task_tracker.breakdown_idx("mark in-progress 7"), 7)

    def test_breakdown_idx_6(self):
        self.assertEqual(task_tracker.breakdown_idx("mark done 3"), 3)

##############################
# breakdown_description(user_input) -> str|None
##############################
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
        self.assertEqual(task_tracker.breakdown_input("add \"Groceries\""), ('add', None, None, 'Groceries'))

    def test_breakdown_input_2(self):
        self.assertEqual(task_tracker.breakdown_input("update 1 \"new task\""), ('update', None, 1, 'new task'))
    
    def test_breakdown_input_3(self):
        self.assertEqual(task_tracker.breakdown_input("delete 1"), ('delete', None, 1, None))

    def test_breakdown_input_4(self):
        self.assertEqual(task_tracker.breakdown_input("mark in-progress 7"), ('mark', 'in-progress', 7, None))

    def test_breakdown_input_5(self):
        self.assertEqual(task_tracker.breakdown_input("mark done 3"), ('mark', 'done', 3, None))

    def test_breakdown_input_6(self):
        self.assertEqual(task_tracker.breakdown_input("list in-progress"), ('list', 'in-progress', None, None))

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
    @patch.object(task_tracker, 'read_from_file', return_value = [])
    def test_file_empty(self, mock_file):
        self.assertTrue(task_tracker.file_empty('tasks.json'))

    @patch.object(task_tracker, 'read_from_file', return_value = None)
    def test_file_empty_2(self, mock_file):
        self.assertTrue(task_tracker.file_empty('tasks.json'))   

    @patch.object(task_tracker, 'read_from_file', return_value = [{'id':1}])
    def test_file_empty_3(self, mock_file):
        self.assertFalse(task_tracker.file_empty('tasks.json'))

##############################
# def update_task(file_tasks, change_idx, data_change, key) -> list:
##############################
    @patch.object(task_tracker, 'get_time', return_value='May 09 2025 13:17:01')
    def test_update_task(self, mock_method):
        self.assertEqual(task_tracker.update_task([{'id': 1, 'status': 'todo'}, {'id': 3, 'status': 'in-progress'}], 3, 'done', 'status'), [{'id': 1, 'status': 'todo'}, {'id': 3, 'status': 'done', 'updatedAt': 'May 09 2025 13:17:01'}])

    @patch.object(task_tracker, 'get_time', return_value='May 09 2025 13:17:01')
    def test_update_task_2(self, mock_method):
        self.assertEqual(task_tracker.update_task([{'id': 1, 'status': 'todo'}, {'id': 3, 'status': 'in-progress'}], 1, 'in-progress', 'status'), [{'id': 1, 'status': 'in-progress', 'updatedAt': 'May 09 2025 13:17:01'}, {'id': 3, 'status': 'in-progress'}])
    
    @patch.object(task_tracker, 'get_time', return_value='May 09 2025 13:17:01')
    def test_update_task_3(self, mock_method):
        self.assertEqual(task_tracker.update_task([{'id': 1, 'description': 'groceries'}, {'id': 3, 'description': 'wash car'}], 1, 'groceries and pharmacy', 'description'), [{'id': 1, 'description': 'groceries and pharmacy', 'updatedAt': 'May 09 2025 13:17:01'}, {'id': 3, 'description': 'wash car'}])
   
    @patch.object(task_tracker, 'get_time', return_value='May 09 2025 13:17:01')
    def test_update_task_4(self, mock_method):
        self.assertEqual(task_tracker.update_task([{'id': 1, 'description': 'groceries'}, {'id': 3, 'description': 'wash car'}], 3, 'wash car and clean interior', 'description'), [{'id': 1, 'description': 'groceries'}, {'id': 3, 'description': 'wash car and clean interior', 'updatedAt': 'May 09 2025 13:17:01'}])

##############################
# def delete_task(file_tasks: list, change_idx) -> list:
##############################
    def test_delete_task(self):
        self.assertEqual(task_tracker.delete_task([{'id': 1}, {'id': 2}, {'id': 3}], 2), [{'id': 1}, {'id': 3}])

    def test_delete_task_2(self):
        self.assertEqual(task_tracker.delete_task([{'id': 1}, {'id': 2}, {'id': 3}], 1), [{'id': 2}, {'id': 3}])
        
if __name__ == "__main__":
    unittest.main()