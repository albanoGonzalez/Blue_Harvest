import requests
import json


def load_json_config(json_path):
    """
    I have created a json to store the parameters for each API. If i would have files I would have added the type for each column, target folder and the unique id.
    The main purpose of this json is just make the code dynamic.
    - in azure I would create a container in the DataLake, with this method I would not have to deploy the code if I either add new columns to the files or I change the folder
    - in AWS I would use the secrets manager
    Load the JSON mapping file

    :param json_path:  path to read the json
    :return: config: parameters in json
    """
    try:
        with open(json_path) as f:
            config = json.load(f)
        print("JSON configuration loaded successfully.")
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found at {json_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON file: {e}")


import time
from requests.exceptions import Timeout, ConnectionError

def api_connection(url, params, retries=3):
    """
    this method will call the url of the api to establish the connection, it will return an error in any case and return the api values.

    :param url: url to connect
    :param params: parameters I need to call the api
    :param retries: number of attempts to connect to the url
    :return: data, error or None
    """

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            print("Connection successful")
            return response.json()
        except (Timeout, ConnectionError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to {url}: {e}")
            return None
    raise RuntimeError(f"Failed to connect to {url} after {retries} attempts")
