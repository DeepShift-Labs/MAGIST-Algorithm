import threading, queue, time, random

def test_thread(item):
	print(f"Starting task... {item}")
	time.sleep(3)
	print(f"Finished task {item}!")

q = queue.PriorityQueue()
# q.put(test_thread)


def worker():
    while True:
        items = q.get()
        items = items[1]
        func = items[0]
        args = items[1:]
        print(f'Working on {args}')
        func(*args)
        print(f'Finished {args}')
        q.task_done()

# Turn-on the worker thread.
threading.Thread(target=worker, daemon=True).start()

# Send thirty task requests to the worker.
for item in range(30):
    q.put((random.randint(1, 30), (test_thread, item)))

# Block until all tasks are done.
q.join()
print('All work completed')