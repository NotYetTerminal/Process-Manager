import subprocess
import time

## signal for wakeing process
SIGCONT: int = 18
## signal for sleeping process
SIGSTOP: int = 19


class ProcessClass:
	"""
	class for process
	stores Popen class
	and is whether the process is sleeping
	"""

	proc: subprocess.Popen = None
	sleeping: bool = False


	def __init__(self: object, new_process: subprocess.Popen) -> object:
		self.proc = new_process
		self.sleeping = False


	def wake_process(self: object) -> None:
		self.proc.send_signal(SIGCONT)


	def sleep_process(self: object) -> None:
		self.proc.send_signal(SIGSTOP)
	

	def kill_process(self: object) -> None:
		self.proc.kill()


## prints out the commands
def print_commands() -> None:
	info: str = """Commands available:
	0 - Exit
	1 - Run process
	2 - Sleep process
	3 - Wake process
	4 - Kill process
	5 - View running processes
	6 - View sleeping processes"""
	print(info)

	return

## asks to stop processes and then quits
def exit_program(process_dictionary: dict) -> None:
	if len(process_dictionary["Running"]) != 0:
		view_running_list(process_dictionary)
		confirmation: str = input("There are running processes, would you ike to kill them? (y / n): ")
		if confirmation == "y":
			for process in process_dictionary["Running"]:
				process.kill_process()
			process_dictionary["Running"] = []

	if len(process_dictionary["Sleeping"]) != 0:
		view_sleeping_list(process_dictionary)
		confirmation: str = input("There are sleeping processes, would you ike to kill them? (y / n): ")
		if confirmation == "y":
			for process in process_dictionary["Sleeping"]:
				process.kill_process()
			process_dictionary["Sleeping"] = []
	
	confirmation: str = input("Are you sure you want to exit? (y / n): ")
	if confirmation == "y":
		quit()
	
	return

## creates new Popen and ProcessClass process
## adds the new ProcessClass to the active list
def create_new_process(process_dictionary: dict) -> None:
	program_name: str = input("Input program name: ")

	## checks if the programm exists
	try:
		new_process: subprocess.Popen = subprocess.Popen([program_name])
	except FileNotFoundError:
		print("Program not found!")
		return
	
	process_dictionary["Running"].append(ProcessClass(new_process))
	print("Process created.")

	return

## sleeps a process and moves them to the sleeping list
def sleep_process(process_dictionary: dict) -> None:
	view_running_list(process_dictionary)
	process_index: int = input("Input process id: ")

	try:
		process_index = int(process_index)
	except:
		print("Not number input!")
		return

	if process_index < len(process_dictionary["Running"]):
		process: ProcessClass = process_dictionary["Running"][abs(process_index)]
		process_dictionary["Running"].remove(process)

		process.sleep_process()
		process_dictionary["Sleeping"].append(process)
		print("Process slept.")
	else:
		print("Id not found!")
	
	return

## sleeps a process and moves them to the running list
def wake_process(process_dictionary: dict) -> None:
	view_sleeping_list(process_dictionary)
	process_index: int = input("Input process id: ")

	try:
		process_index = int(process_index)
	except:
		print("Not number input!")
		return

	if process_index < len(process_dictionary["Sleeping"]):
		process: ProcessClass = process_dictionary["Sleeping"][abs(process_index)]
		process_dictionary["Sleeping"].remove(process)

		process.wake_process()
		process_dictionary["Running"].append(process)
		print("Process continued.")
	else:
		print("Id not found!")
	
	return

## kills a process and removes it from its respective list
def kill_process(process_dictionary: dict) -> None:
	view_running_list(process_dictionary)
	process_index: int = input("Input process id (or press enter to skip): ")

	try:
		process_index = int(process_index)
	except:
		if process_index != "\n":
			print("Not number input!")
		process_index = "\n"

	if process_index == "\n":
		pass
	elif process_index < len(process_dictionary["Running"]):
		process: ProcessClass = process_dictionary["Running"][abs(process_index)]
		process_dictionary["Running"].remove(process)

		process.kill_process()
		print("Process killed.")
	else:
		print("Id not found!")
	
	view_sleeping_list(process_dictionary)
	process_index: int = input("Input process id (or press enter to skip): ")

	try:
		process_index = int(process_index)
	except:
		if process_index != "\n":
			print("Not number input!")
		process_index = "\n"

	if process_index == "\n":
		pass
	elif process_index < len(process_dictionary["Sleeping"]):
		process: ProcessClass = process_dictionary["Sleeping"][abs(process_index)]
		process_dictionary["Sleeping"].remove(process)

		process.kill_process()
		print("Process killed.")
	else:
		print("Id not found!")
	
	return

## print out the running processes
def view_running_list(process_dictionary: dict) -> None:
	print("Running processes:")
	if len(process_dictionary["Running"]) == 0:
		print("None")
	else:
		for index in range(len(process_dictionary["Running"])):
			print(f"{index} - {process_dictionary['Running'][index].proc.args}")
	
	return

## print out the sleeping processes
def view_sleeping_list(process_dictionary: dict) -> None:
	print("Sleeping processes:")
	if len(process_dictionary["Sleeping"]) == 0:
		print("None")
	else:
		for index in range(len(process_dictionary["Sleeping"])):
			print(f"{index} - {process_dictionary['Sleeping'][index].proc.args}")
	
	return


def main() -> None:
	process_dictionary = {"Running": [],
						  "Sleeping": []}

	while True:
		print_commands()
		input_command: int = input("Input command number: ")

		try:
			input_command = int(input_command)
		except:
			print("Not number input!")
			continue

		if input_command == 0:
			exit_program(process_dictionary)
		elif input_command == 1:
			create_new_process(process_dictionary)
		elif input_command == 2:
			sleep_process(process_dictionary)
		elif input_command == 3:
			wake_process(process_dictionary)
		elif input_command == 4:
			kill_process(process_dictionary)
		elif input_command == 5:
			view_running_list(process_dictionary)
		elif input_command == 6:
			view_sleeping_list(process_dictionary)
		else:
			print("Command not found!")
		
		input("Press enter to continue...")
	
	return


if __name__ == "__main__":
	main()

