import logging
import json
import os, pathlib

class MainLogger():
    def __init__(self, config):
        config = pathlib.Path(config)
        config = config.resolve()
        f = open(config)
        config = json.load(f)

        for i in config['paths']:
            self.log_dir = i["log_dir"]
        for i in config['basic_variables']:
            self.verbose = i["verbose"]

    def StandardLogger(self, name):
        logger = logging.getLogger(name)
        if not self.verbose:
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

        print(f"LogMaster Initialized Successfully ===> {os.path.join(self.log_dir, 'complete.log')}")

        return logger



