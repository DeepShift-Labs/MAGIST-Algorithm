from multiprocessing import Pool, cpu_count
import threading

thread_waitlist = []
thread_executing_registry = []
max_thread_per_core = 1
max_cpu_count = cpu_count()

print("CPU count:", cpu_count())


def execute_thread(thread_instance):
	thread_waitlist.remove(thread_instance)
	thread_executing_registry.append(thread_instance)
	thread_instance.start()

def delete_thread(thread_instance):
	thread_executing_registry.remove(thread_instance)
	thread_instance.join()

def append_threads(*args):
	for i in args:
		thread_waitlist.append(i)

def die(thread_executing_registry, self_instance):
	init = 4
	for i in range(25):
		init = init * init
	thread_executing_registry.remove()

x0 = threading.Thread(target=die)

x1 = threading.Thread(target=die)

x2 = threading.Thread(target=die)

x3 = threading.Thread(target=die)

x4 = threading.Thread(target=die)

x5 = threading.Thread(target=die)

x6 = threading.Thread(target=die)

append_threads(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

print("Threads waiting:", len(thread_waitlist))

core_usage = 0

while len(thread_waitlist) > 0 or core_usage >= max_cpu_count:
	tasks_for_core = thread_waitlist[0:max_thread_per_core]
	for i in tasks_for_core:
		print("Executing thread:", i)
		thread_waitlist.remove(i)
		thread_executing_registry.append(i)
	print("Core MAXED")
	core_usage += 1