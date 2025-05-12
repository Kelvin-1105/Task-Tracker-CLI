import json
import re
import os.path
import datetime

def main() -> None:
	file = "tasks.json" # refactor in test_cases.py aswell
	if file_exists(file) and not file_empty(file): # ensure an existing non-empty file 
		curr_id = find_id(file) + 1
	else:
		write_to_file(file, [])
		curr_id = 1

	while True:
		try:
			primary_keyword, secondary_keyword, change_idx, description = breakdown_input(get_input())
			
			if primary_keyword == 'add':
				if empty_variable([description]):
					raise TypeError(f"Description={description}, invalid input")
				
				new_task = add_task(description, curr_id)
				file_tasks = read_from_file(file)
				merged_tasks = merge_tasks(file_tasks, new_task)

				write_to_file(file, merged_tasks)
				print(f'Task added successfully (ID: {curr_id})')
				curr_id += 1 

			elif primary_keyword == 'update':
				if empty_variable([change_idx, description]):
					raise TypeError(f"Index={change_idx}, Description={description}, invalid input")
				
				file_tasks = read_from_file(file)
				arranged_tasks = update_task(file_tasks, change_idx, description, 'description')

				write_to_file(file, arranged_tasks)
				print(f'Task updated (ID: {change_idx})')

			elif primary_keyword == 'mark':
				if empty_variable([change_idx, secondary_keyword]):
					raise TypeError(f"index={change_idx} or secondary_keyword={secondary_keyword}, invalid input")
				
				file_tasks = read_from_file(file)
				arranged_tasks = update_task(file_tasks, change_idx, secondary_keyword, 'status')

				write_to_file(file, arranged_tasks)
				print(f'Task updated (ID: {change_idx})')

			elif primary_keyword == 'delete':
				if empty_variable(change_idx):
					raise TypeError(f"Index={change_idx}, invalid input")		
				
				file_tasks = read_from_file(file)
				arranged_tasks = delete_task(file_tasks, change_idx)

				write_to_file(file, arranged_tasks)	
				print(f'Task deleted')

			elif primary_keyword == 'list':
				tasks_dict = list_tasks(file, secondary_keyword)
				print_tasks(tasks_dict)

			elif primary_keyword == 'esc':
				exit()

			else:
				raise TypeError(f"primary_keyword={primary_keyword}, invalid input")
			
		except TypeError as e:
			print(str(e))

# given index, delete specified task
def delete_task(file_tasks: list, change_idx) -> list:
	for i in range(0, len(file_tasks)-1):
		if file_tasks[i]['id'] == change_idx:
			del file_tasks[i]
	return file_tasks

# given index, change status or description
def update_task(file_tasks, change_idx, data_change, key) -> list:
	for task in file_tasks:
		if task['id'] == change_idx:
			formatted_time = get_time()
			task[key] = data_change
			task['updatedAt'] = formatted_time
	return file_tasks

# get and format date and time
def get_time():
	curr_time = datetime.datetime.now()
	return curr_time.strftime("%b %d %Y %H:%M:%S")

# ensure no variable is of None type, or equivalent state
def empty_variable(necessary_input_list: list):
	for necessary_input in necessary_input_list:
		if necessary_input == None:
			return True
	return False

# create task, as dict
def add_task(description, curr_id) -> dict:
	formatted_time = get_time()
	new_task = {
		"id": curr_id,
		"description": description,
		"status": "todo",
		"createdAt": formatted_time,
		"updatedAt": formatted_time
	}
	return new_task

# print tasks, listing index and description
def print_tasks(tasks_dict):
	for idx, description in tasks_dict.items():
		print(f'{idx}. {description}')

# return tasks to list, given criteria (done, in-progress, todo) or assuming all
def list_tasks(file, secondary_keyword) -> dict:
	if secondary_keyword == None:
		secondary_keyword = ['done', 'todo', 'in-progress']
	elif secondary_keyword not in ['done', 'todo', 'in-progress']:
		raise TypeError(f"secondary_keyword={secondary_keyword}, invalid input")
	
	tasks = read_from_file(file)
	tasks_dict = {}
	for task in tasks:
		if task['status'] in secondary_keyword:
			tasks_dict[task['id']] = task['description']
	return tasks_dict

# ensure file is not empty
def file_empty(file) -> bool:
	tasks = read_from_file(file)
	return not tasks

# merge tasks in file with created task
def merge_tasks(file_tasks, new_task) -> list:
	file_tasks.append(new_task)
	return file_tasks

# find largest id in file
def find_id(file) -> int|None: 
	tasks = read_from_file(file)
	max_idx = 0
	for task in tasks:
		if task["id"] > max_idx:
			max_idx = task["id"]
	return max_idx

# ensure file exists
def file_exists(file) -> bool: 
	if not os.path.isfile(file):
		write_to_file(file, [])
		return False
	return True

def get_input() -> str: 
	return input()

# breakdown user input into tokens
def breakdown_input(user_input) -> list[str|None, str|None, int|None, str|None]: 
	primary_keyword, secondary_keyword= breakdown_keywords(user_input)
	idx = breakdown_idx(user_input)
	description = breakdown_description(user_input)
	return primary_keyword, secondary_keyword, idx, description

# from user input, return index
def breakdown_idx(user_input) -> int|None: 
	# regex cleans keyword, [a-z], then cleans secondary_keyword, [a-z] including hyphens
	regex_dict = {0: r'^[a-z]+', 1: r'^[a-z]+(?:-\w+)*'}
	cleaned = user_input
	for i in range(0, 2):
		try:
			cleaned = re.sub(regex_dict[i], '', cleaned)
			cleaned = re.sub(r'^\s', '', cleaned) # strip whitespace after word
		except: 
			continue

	idx = re.match(r"^\d+", cleaned) # matches a number
	return None if not idx else int(idx.group(0)) # return None if idx has no value, else return idx

# from user input, return description
def breakdown_description(user_input) -> str|None: 
	# regex matches text between apostrophes or quotation marks
	description = re.findall(r"(?<=['\"])(.*?)(?=['\"])", user_input)
	return None if not description else ''.join(description) # return None if description has no value, else return description
# from user input return keywords
def breakdown_keywords(user_input) -> list[str|None, str|None]: 
	# regex - matches first word
	primary_keyword = re.match(r'^[a-z]+', user_input)
	try: # try to find a secondary keyword
		cleaned = re.sub(r'^[a-z]+', '', user_input) # strip first word
		cleaned = re.sub(r'^\s', '', cleaned) # strip whitespace after first word
		secondary_keyword = re.match(r'^[a-z]+(?:-\w+)*', cleaned) # match word, include hyphen
	except: # only runs when there is no secondary_keyword
		return [None, None] if not primary_keyword else [primary_keyword.group(0), None] # return [None, None] if primary_keyword has no value, else return [primary_keyword, None]

	primary_keyword = None if not primary_keyword else primary_keyword.group(0) # return None if primary_keyword has no value, else return primary_keyword
	secondary_keyword = None if not secondary_keyword else secondary_keyword.group(0) # return None if secondary_keyword has no value, else return secondary_keyword
	return primary_keyword, secondary_keyword


def write_to_file(file, data) -> None: 
	with open(file, 'w') as f:
		json.dump(data, f, indent=2)

def read_from_file(file) -> list|None: 
	with open(file, 'r') as f: 
		return json.load(f)

if __name__ == "__main__":
	main()

