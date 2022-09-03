"""Establish major logger functions for individual scripts.

MainLogger is the main class containing 1 main function that provides a unique logging instance to each script.
"""

import logging
import json
import os
import pathlib


class CustomFormatter(logging.Formatter):

    blue = '\033[34m'
    green = '\033[92m'
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: blue + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class MainLogger():
    # Logging Class

    def __init__(self, config):
        """Initialize class and parse config

        :param config: A relative or absolute path to master config JSON file.
        """
        config = pathlib.Path(config)
        config = config.resolve()  # Find absolute path from a relative one.
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

        self.log_dir = pathlib.Path(self.log_dir)
        # Find absolute path from a relative one.
        self.log_dir = self.log_dir.resolve()
        self.log_dir = str(self.log_dir)

    def StandardLogger(self, name):
        logger = logging.getLogger(name)
        if not self.verbose:  # Enable verbose depending on flag set by the config file.
            logger.setLevel(logging.WARNING)
        else:
            logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        try:
            fh = logging.FileHandler(
                os.path.join(
                    self.log_dir,
                    'complete.log'))
        except FileNotFoundError:
            os.makedirs(self.log_dir)
            fh = logging.FileHandler(
                os.path.join(
                    self.log_dir,
                    'complete.log'))

        # create console handler with a higher log level
        error = logging.StreamHandler()

        error.setFormatter(CustomFormatter())

        # create formatter and add it to the handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        # error.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(error)

        logger.info(
            f"{name}'s LogMaster Instance Initialized Successfully ===> {os.path.join(self.log_dir, 'complete.log')}")

        return logger
