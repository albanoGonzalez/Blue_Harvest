from Functions.connections import (
    load_json_config,
    api_connection
)
from Functions.data import (
    get_names,
    get_comics_character
)
import requests
from hashlib import md5
import pandas as pd
def main():
    mapping = load_json_config("../mapping_apis.json")
    api_list = mapping["api_list"]
    # show each api
    for api in api_list:
        url = f"{api['base_url']}{api['endpoint']}"
        print(f"Base URL: {url}")
        ts = api["params"]["ts"]
        public_key = api["params"]["public_key"]
        private_key = api["params"]["private_key"]
        params = {
            "apikey": api["params"]["public_key"],
            "ts": api["params"]["ts"],
            "hash": md5(f"{ts}{private_key}{public_key}".encode("utf8")).hexdigest()
        }
        print(params)
        if api['endpoint'] == "/characters":
            values = api_connection(url, params=params)
            print("characters")
            characters = get_names(values)
            print(characters)
        elif api['endpoint'] == "/comics" and characters:
            print("comics")
            for i in characters:
                params['characters'] = "1011334"
                values = api_connection(url, params=params)
                print(values)
                comics = get_comics_character(characters,values)
                print(comics)
if __name__ == "__main__":
    main()