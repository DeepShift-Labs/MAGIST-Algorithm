"""Threaded Queue contains all necessary functions for a priority queue.

The queue class contains methods to add, execute, thread, and process tasks in a queue based on a priority system.
"""

import queue
import threading
import uuid
import json
import pathlib
import numpy as np

from ..Utils.LogMaster.log_init import MainLogger


class MainPriorityQueue():
    """Main Priority Queue Class."""

    def __init__(self, config):
        """Initialize the queue.

        :param config: The config file(config.json).
        """

        self.guid = uuid.uuid4()
        self.q = queue.PriorityQueue()

        root_log = MainLogger(config)
        # Create a script specific logging instance
        self.log = root_log.StandardLogger("QueueController")

        self.function_returns = []

        config = pathlib.Path(config)
        config = config.resolve()  # Find absolute path from a relative one.
        with open(config) as f:
            config = json.load(f)

        for i in config['task_management']:
            try:
                self.worker_threads = i["num_of_worker_threads"]
            except KeyError:
                pass

    def __worker(self):
        """The worker thread. This actually executes the tasks in the queue.
        """

        while True:
            items = self.q.get()
            items = items[1]
            func = items[0]
            args = items[1:]
            # print(f'Working on {args}')

            last_item = args[-1]  # name
            second_last_item = args[-2]  # priority
            third_last_item = args[-3]  # guid

            args = args[:len(args) - 3]

            self.log.info(
                f'Received task: {last_item} with priority {second_last_item}. '
                f'Unique ID assigned: {third_last_item}. Executing...')
            [*returns] = [func(*args)]
            self.log.info(f'Finished {last_item} successfully.')
            self.q.task_done()
            returns = np.array(returns)
            self.function_returns.append([third_last_item, returns])
            # self.function_returns = np.squeeze(self.function_returns)

    def put_queue(self, function, *args, name="Unnamed", priority=None):
        """Add a task to the queue.

        :param function: The function to be executed. NOTE: This must be in the form of Class.put_queue(function...),
        not Class.put_queue(function()...).
        :param args: The arguments to be passed to the function. This can be any number of args.
        :param name: The name of the task.
        :param priority: The priority of the task.

        :return: The unique ID of the task.
        """

        args = list(args)

        for i in args:
            if i in (name, priority):
                raise ValueError(
                    "Name or priority cannot be used as argument. Please use priority= and name= in the function call.")

        self.q.put((priority, (function, *args, self.guid, priority, name)))

        return self.guid

    def detach_thread(self):
        """Detach the thread from the main thread.
        """

        # Turn-on the worker thread.
        for i in range(self.worker_threads):
            threading.Thread(target=self.__worker, daemon=True).start()
        self.log.info("Thread created and daemonized. Queue started...")

    def join_thread(self):
        """Join the queue thread with main.
        """

        self.log.info("Attempting to join main thread...")
        self.q.join()
        self.log.info("Queue merge finished.")

    def search_results(self, query):
        """Search the results for a specific task by ID.

        :param query: The unique ID of the task. NOTE: This must be a UUID object.

        :return: The results of the task.
        """

        r = self.function_returns
        r = np.array(r)
        r = r[r[:, 0] == query]
        r = np.squeeze(r)

        return np.squeeze(r[1])
