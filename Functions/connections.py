import requests
import json

def load_json_config(json_path):
    """
    I have created a json to store the APIs the columns. If i would have files I would have added type for each column, target folder and the unique id.
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


def api_connection(url, params):
    """
    this method will call the url of the api to establish the connection. it will return an error in any case and will return the values in the api.
    :param url: api url to connect
    :param params: parameters i need to call the api
    :return:
    """
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print("Connection successful")
            return response.json()
        else:
            print(f"Status error {url}: {response.status_code}")
    except requests.exceptions.RequestException as e:
            print(f"Connection error {url}: {e}")