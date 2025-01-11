from hashlib import md5
from Functions.connections import (
    api_connection
)
def get_all_values(api):
    """
    Get all the data from the API, multiple calls, you just can read 100 records each call
    :param api_list: it contains the fields and the url to make the call
    :return: list with the data
    """
    all_results = []
    url = f"{api['base_url']}{api['endpoint']}"
    print(f"Llamando a la API: {url}")
    ts = api["params"]["ts"]
    public_key = api["params"]["public_key"]
    private_key = api["params"]["private_key"]
    params = {
        "apikey": public_key,
        "ts": ts,
        "hash": md5(f"{ts}{private_key}{public_key}".encode("utf8")).hexdigest(),
        "limit": 100,
        "offset": 0,
    }

    while True:
        values = api_connection(url, params=params)
        results = values["data"]["results"]
        all_results.extend(results)

        #len lower than the limit we stop because we do not have more data to red, also i can use the total field in the API.
        if len(results) < params["limit"]:
            break
        params["offset"] += params["limit"]

    return all_results

def get_all_values_comics(api, id):
    """
    Get all the comics for each character
    :param api_list: it contains the fields and the url to make the call
    :param id: id for the character
    :return: int (total number of comics for this character)
    """
    url = f"{api['base_url']}{api['endpoint']}"
    print(f"Llamando a la API: {url}")
    ts = api["params"]["ts"]
    public_key = api["params"]["public_key"]
    private_key = api["params"]["private_key"]
    params = {
        "apikey": public_key,
        "ts": ts,
        "hash": md5(f"{ts}{private_key}{public_key}".encode("utf8")).hexdigest(),
        "characters": id,
        "limit": 100,
        "offset": 0
    }

    values = api_connection(url, params=params)
    total = values['data']['total']

    return total

def get_names(all_data):
    """
    get the name and id for all the characters in the api

    :param values: data from the API
    :return: a list consisting of the id and the name of the character
    """
    unique_names = set()  # avoid duplicates
    for char in all_data:
        unique_names.add((char['id'], char['name'], char["comics"]["available"]))
    return unique_names

