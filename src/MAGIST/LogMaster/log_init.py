"""Establish major logger functions for individual scripts.

MainLogger is the main class containing 1 main function that provides a unique logging instance to each script.
"""

import logging
import json
import os, pathlib

class MainLogger():
    # Logging Class

    def __init__(self, config):
        """Initialize class and parse config

        :param config: A relative or absolute path to master config JSON file.
        """
        config = pathlib.Path(config)
        config = config.resolve() # Find absolute path from a relative one.
        f = open(config)
        config = json.load(f)

        for i in config['paths']:
            try:
                self.log_dir = i["log_dir"]
            except KeyError:
                pass
        for j in config['basic_variables']:
            try:
                self.verbose = j["verbose"]
            except KeyError:
                pass

    def StandardLogger(self, name):
        logger = logging.getLogger(name)
        if not self.verbose: # Enable verbose depending on flag set by the config file.
            logger.setLevel(logging.WARNING)
        else:
            logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(os.path.join(self.log_dir, 'complete.log'))

        # create console handler with a higher log level
        error = logging.StreamHandler()

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        error.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(error)

        logger.info(f"{name}'s LogMaster Instance Initialized Successfully ===> {os.path.join(self.log_dir, 'complete.log')}")

        return logger



