import subprocess
import time


SIGCONT: int = 18
SIGSTOP: int = 19


class ProcessClass:

	proc: subprocess.Popen = None
	sleeping: bool = False


	def __init__(self: object, new_process: subprocess.Popen) -> object:
		self.proc = new_process
		self.sleeping = False


	def continue_process(self: object) -> None:
		self.proc.send_signal(SIGCONT)


	def stop_process(self: object) -> None:
		self.proc.send_signal(SIGSTOP)
	

	def kill_process(self: object) -> None:
		self.proc.kill()


def create_new_process(program_name: str, active_list: list) -> int:

	new_process: subprocess.Popen = subprocess.Popen([program_name])
	active_list.append(new_process)

	return 0


def setup() -> None:
	process_active_list: list = []
	pricess_sleeping_list: list = []

	return_code: int = create_new_process("gnome-text-editor", process_active_list)

	print(return_code)



if __name__ == "__main__":
	setup()
