# Task-Tracker-CLI
This is a CLI-based task manager. Tasks are stored locally, via .json file. User may adjust descriptions of task, status of task (todo, in-progress, or done), delete a task, and/or list all tasks (allowing for speceficity to those of only certain status). User input is broken down via regex, and undergoes multiple layers of input validation to ensure a smooth running experience. Take the first step into a more productive day!

### How to use:
Add task: `add "{description}"`
Update task: `update {index} "{new_description}"`
Mark task: `mark {todo, done, in-progress}`
Delete task: `delete {index}`
List tasks: `list {None: lists all tasks, todo, done, in-progress}`
