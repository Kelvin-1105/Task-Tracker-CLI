tasks = [{'status': 'thing', 'id': 1, 'description': 'first thing'}, 
		 {'status': 'not thing', 'id': 2, 'description': 'second thing'}]
task_dict = {}
for task in tasks:
	if task['status'] in ['thing', 'not thing']:
		task_dict[task['id']] = task['description']

for idx, description in task_dict.items():
	print(f'{idx}. {description}')

