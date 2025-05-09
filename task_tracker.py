import json
import re
import os.path
import datetime
'''
todo list:
		printing output
'''
def main() -> None:
	file = "tasks.json" # if change, change in test_cases 
	if file_exists(file) and not file_empty(file):
		curr_id = find_id(file) + 1
	else:
		write_to_file(file, [])
		curr_id = 1

	while True:
		primary_keyword, secondary_keyword, change_idx, description = breakdown_input(get_input())
		
		if primary_keyword == 'add':
			if empty_variable([description]):
				raise TypeError("Description is null")
			new_task = add_task(description, curr_id)
			file_tasks = read_from_file(file)
			merged_tasks = merge_tasks(file_tasks, new_task)
			write_to_file(file, merged_tasks)
			curr_id += 1 

		elif primary_keyword == 'list':
			tasks_dict = list_tasks(file, secondary_keyword)
			print_tasks(tasks_dict)

		elif primary_keyword == 'mark':
			if empty_variable([change_idx, secondary_keyword]):
				raise TypeError("Index or Secondary keyword is null")
			file_tasks = read_from_file(file)
			arranged_tasks = update_task(file_tasks, change_idx, secondary_keyword, 'status')
			write_to_file(file, arranged_tasks)

		elif primary_keyword == 'delete':
			if empty_variable(change_idx):
				raise TypeError("Index is null")
			file_tasks = read_from_file(file)
			arranged_tasks = delete_task(file_tasks, change_idx)
			write_to_file(file, arranged_tasks)

		elif primary_keyword == 'update':
			if empty_variable([change_idx, description]):
				raise TypeError("Index or Description is null")
			file_tasks = read_from_file(file)
			arranged_tasks = update_task(file_tasks, change_idx, description, 'description')
		elif primary_keyword == 'esc':
			exit()
		else:
			print("Invalid Input")

def delete_task(file_tasks: list, change_idx) -> list:
	for i in range(0, len(file_tasks)-1):
		if file_tasks[i]['id'] == change_idx:
			del file_tasks[i]
	return file_tasks

def update_task(file_tasks, change_idx, data_change, key) -> list:
	for task in file_tasks:
		if task['id'] == change_idx:
			task[key] = data_change
	return file_tasks

def empty_variable(necessary_input_list: list):
	for necessary_input in necessary_input_list:
		if necessary_input == None:
			return True
	return False

def add_task(description, curr_id) -> dict:
	curr_time = datetime.datetime.now()
	new_task = {
		"id": curr_id,
		"description": description,
		"status": "todo",
		"createdAt": curr_time.strftime("%b %d %Y %H:%M:%S"),
		"updatedAt": curr_time.strftime("%b %d %Y %H:%M:%S")
	}
	return new_task


def print_tasks(tasks_dict):
	for idx, description in tasks_dict.items():
		print(f'{idx}. {description}')

def list_tasks(file, secondary_keyword) -> dict:
	tasks = read_from_file(file)
	if secondary_keyword == None:
		secondary_keyword = ['done', 'todo', 'in-progress']
	elif secondary_keyword not in ['done', 'todo', 'in-progress']:
		raise TypeError("Invalid Input")
	task_dict = {}
	for task in tasks:
		if task['status'] in secondary_keyword:
			task_dict[task['id']] = task['description']
	return task_dict

def file_empty(file) -> bool:
	tasks = read_from_file(file)
	return is_empty(tasks)

def is_empty(tasks) -> bool:
	return not tasks

def merge_tasks(file_tasks, new_task) -> list:
	file_tasks.append(new_task)
	return file_tasks

def find_id(file) -> int|None: 
	tasks = read_from_file(file)
	max_idx = 0
	for task in tasks:
		if task["id"] > max_idx:
			max_idx = task["id"]
	return max_idx

def file_exists(file) -> bool: 
	if not os.path.isfile(file):
		write_to_file(file, [])
		return False
	return True

def get_input() -> str: 
	user_input = input()
	if user_input:
		return user_input
	print("Invalid Input")
	exit()

def breakdown_input(user_input) -> list[str|None, str|None, int|None, str|None]: 
	primary_keyword, secondary_keyword= breakdown_keywords(user_input)
	idx = breakdown_idx(user_input)
	description = breakdown_description(user_input)
	return primary_keyword, secondary_keyword, idx, description

def breakdown_idx(user_input) -> int|None: 
	# regex matches numbers after the first word but before an apostrophe or quotation mark
	regex_dict = {0: r'^[a-z]+', 1: r'^[a-z]+(?:-\w+)*'}
	cleaned = user_input
	for i in range(0, 2):
		try:
			cleaned = re.sub(regex_dict[i], '', cleaned)
			cleaned = re.sub(r'^\s', '', cleaned)
		except: 
			continue

	idx = re.match(r"^(\d+)(?=['\"]?)", cleaned)
	return None if not idx else int(idx.group(0))

def breakdown_description(user_input) -> str|None: 
	# regex matches all between apostrophes or quotation marks
	description = re.findall(r"(?<=['\"])(.*?)(?=['\"])", user_input)
	return None if not description else ''.join(description)

def breakdown_keywords(user_input) -> list[str|None, str|None]: 
	# regex - matches first word
	primary_keyword = re.match(r'^[a-z]+', user_input)
	try:
		cleaned = re.sub(r'^\w+', '', user_input) # strip first word
		cleaned = re.sub(r'^\s', '', cleaned) # strip whitespace after first word
		secondary_keyword = re.match(r'^[a-z]+(?:-\w+)*', cleaned)
	except:
		return [None, None] if not primary_keyword else [primary_keyword.group(0), None]

	primary_keyword = None if not primary_keyword else primary_keyword.group(0)
	secondary_keyword = None if not secondary_keyword else secondary_keyword.group(0)
	return primary_keyword, secondary_keyword

def write_to_file(file, data) -> None: 
	with open(file, 'w') as f:
		json.dump(data, f, indent=2)

def read_from_file(file) -> list|None: 
	with open(file, 'r') as f: 
		return json.load(f)

if __name__ == "__main__":
	main()

