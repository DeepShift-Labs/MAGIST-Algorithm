import requests
import json

from ..Utils.LogMaster.log_init import MainLogger


class ClassDeprecated(Exception):
    pass


class UrbanDictionary():
    def __init__(self, config):
        """Initialize the Urban Dictionary API.
        :param config: The config file(config.json).
        """

        raise ClassDeprecated("This class is deprecated")

        root_log = MainLogger(config)
        self.log = root_log.StandardLogger("UrbanDictionary")

        self.url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

    def define(self, word):
        """Define a word.
        :param word: The word to be defined.
        :return: The definition of the word.
        """

        querystring = {"term": word}

        headers = {
            "X-RapidAPI-Key": "xxx",
            "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"}

        response = requests.request(
            "GET", self.url, headers=headers, params=querystring)

        json_data = json.loads(response.text)

        definition = json_data["list"][0]["definition"]

        self.log.info(f"Definition of {word}: " + definition)

        return definition


class DicitonaryAPIDev():
    def __init__(self, config):
        """Initialize the Dictionary API..

        :param config: The config file(config.json).
        """

        root_log = MainLogger(config)
        self.log = root_log.StandardLogger("DisctionaryAPI")

        self.url = "https://api.dictionaryapi.dev/api/v2/entries/en/"

    def define(self, word):
        """Define a word.

        :param word: The word to be defined.

        :return: The definition of the word.
        """

        querystring = {"term": word}

        self.url = self.url + word

        response = requests.request("GET", self.url, params=querystring)

        json_data = json.loads(response.text)

        definition = json_data
        try:
            definition = definition[0]["meanings"][0]["definitions"][0][
                "definition"]
        except KeyError:
            definition = "No definition found"

        self.log.info(f"Definition of {word}: " + definition)

        self.url = "https://api.dictionaryapi.dev/api/v2/entries/en/"

        return definition


class FullDictionarySearch():
    def __init__(self, config):
        """Initialize the Dictionary API..

        :param config: The config file(config.json).
        """

        root_log = MainLogger(config)
        self.log = root_log.StandardLogger("FullDictionarySearch")

        self.dictdev = DicitonaryAPIDev(config)

    def define(self, word):
        definition = self.dictdev.define(word)

        if definition == "No definition found":
            self.log.info("No definition found in DictionaryAPI.dev.")
            definition = None

        return definition
