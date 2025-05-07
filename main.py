import json
import re
import os.path
import datetime


def main():
	file = "tasks.json"
	if file_exists(file):
		curr_id = find_id(file) # todo
	else: 
		curr_id = 1
	
	# while isContinue:
	keyword, change_idx, description = breakdown_input(get_input())
	if keyword == 'add':
		curr_time = datetime.datetime.now()
		new_task = {
			"id": curr_id,
			"description": description,
			"status": "todo",
			"createdAt": curr_time.strftime("%b %d %Y %H:%M:%S"),
			"updatedAt": curr_time.strftime("%b %d %Y %H:%M:%S")
		}
		curr_id+=1
		file_tasks = read_from_file(file)
		merged_tasks = merge_tasks(file_tasks, new_task)
		write_to_file(file, merged_tasks)
	# elif keyword == 'update':

	# 	write_to_file(file)

##############################
# delete this later
		# try:
		# 	if keyword == 'add':
		# 		# check description isn't empty
		# 		write_to_file(f"{curr_id}.{description}")
		# 	elif keyword == 'update':
		# 		if is_none(idx) or is_none(description):
		# 			raise TypeError("Invalid input", f'idx={idx}', f'description={description}')
		# 		write_to_file(f"{idx}.{description}") # todo: learn how to overwrite a line
		# 	elif keyword == 'delete':
		# 		write_to_file(f"") # todo: learn how to delete a line, but keep it spaced (to not impact other ids)
			
		# except ValueError as error: 
		# 	print(error.args)
##############################
def merge_tasks(file_tasks, new_task) -> list: 
	file_tasks.append(new_task)
	return file_tasks

def find_id(file) -> int:
	tasks = read_from_file(file)
	idx = 0
	for task in tasks:
		if task["id"] > idx:
			idx = task["id"] + 1
	return idx

def file_exists(file):
	if not os.path.isfile(file):
		write_to_file(file, [])
		return False
	return True

def get_input() -> str:
	return input()

def breakdown_input(user_input) -> list[str|None, int|None, str|None]:
	keyword = breakdown_keyword(user_input)
	idx = breakdown_idx(user_input)
	description = breakdown_description(user_input)
	return keyword, idx, description

def breakdown_idx(user_input) -> int|None:
	# regex matches numbers after the first word but before an apostrophe or quotation mark
	idx = re.match(r"^\w+\s(\d+)(?=['\"]?)", user_input)
	return None if not idx else int(idx.group(1))

def breakdown_description(user_input) -> str|None:
	# regex matches all between apostrophes or quotation marks
	description = re.findall(r"(?<=['\"])(.*?)(?=['\"])", user_input)
	return None if not description else ''.join(description)

def breakdown_keyword(user_input) -> str|None:
	# regex - matches first word
	keyword = re.match(r'^\w+', user_input)
	return None if not keyword else keyword.group(0)

def write_to_file(file, data):
	with open(file, 'w') as f:
		json.dump(data, f, indent=2)

def read_from_file(file):
	with open(file, 'r') as f: 
		return json.load(f)

if __name__ == "__main__":
	main()

