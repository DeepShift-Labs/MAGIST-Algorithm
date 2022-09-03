"""Mongo Utils file that manages and initializes the MongoDB connection.

This file contains the main Admin functions and the rest is done using the PrimaryNeuralDB file.
"""

import json
import os
import pathlib

import pymongo as mongo

from ..Utils.LogMaster.log_init import MainLogger


class AdminUtils():
    """Class that manages the MongoDB connection."""

    def __init__(self, config):
        """Initialize the AdminUtils class.

        :param config: The config file(string).
        """

        root_log = MainLogger(config)
        # Create a script specific logging instance
        self.log = root_log.StandardLogger("MongoAdminUtils")

        self.log.info("Firing up MongoDB Neural Database! Standby...")

        config = pathlib.Path(config)
        config = config.resolve()  # Find absolute path from a relative one.
        with open(config) as f:
            config = json.load(f)

        for i in config['system_administration']:
            try:
                self.passcode = i["sudo_password"]
            except KeyError:
                pass

        for j in config['neural_db']:
            try:
                self.mgsocket = j["mongo_socket"]
            except KeyError:
                pass

        self.db_client = mongo.MongoClient(self.mgsocket)

    def initialize_neuraldb(self):
        """Initialize the MongoDB connection.

        :return: The MongoDB client.
        """

        command = 'systemctl start mongod'
        p = os.system(f'echo {self.passcode}|sudo -S {command}')
        self.log.info(
            "NeuralDB Launched Successfully! Attempting to connect to local socket...")

        if self.db_client:
            self.log.info(
                "Mongo client linked successfully. Local DB Agent is running.")
        else:
            self.log.error(
                "Mongo client failed to connect. The Mongo socket URL could be incorrect. It should look "
                "something like this: mongodb://localhost:27017/")

        return self.db_client

    def stop_db(self):
        """Stop the MongoDB connection.
        """

        self.log.info("Shutting down MongoDB Neural Database! Standby...")
        command = 'systemctl stop mongod'
        p = os.system('echo %s|sudo -S %s' % (self.passcode, command))
        self.log.info("NeuralDB Closed Successfully!")

    def restart_db(self):
        """Restart the MongoDB connection.
        """

        self.log.info("Restarting MongoDB Neural Database! Standby...")

        command = 'systemctl restart mongod'
        p = os.system('echo %s|sudo -S %s' % (self.passcode, command))
        self.log.info(
            "NeuralDB Re-Launched Successfully! Attempting to connect to local socket...")

        if self.db_client:
            self.log.info(
                "Mongo client linked successfully. Local DB Agent is running.")
        else:
            self.log.error(
                "Mongo client failed to connect. The Mongo socket URL could be incorrect. It should look "
                "something like this: mongodb://localhost:27017/")

        return self.db_client
