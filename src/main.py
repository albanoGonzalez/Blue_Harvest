from Functions.connections import (
    load_json_config,
    api_connection
)
from Functions.data import (
    get_all_values,
    get_all_values_comics,
    get_names
)
import pandas as pd
def main():
    mapping = load_json_config("../mapping_apis.json")
    api_list = mapping["api_list"]
    for api in api_list:
        if api['endpoint'] == "/characters":
            all_data = get_all_values(api)
            print(f"Total data: {len(all_data)}")
            characters_comics = get_names(all_data)
            for id, name, total in characters_comics:
                print(f"Character name: {name} - quantity of comics they appear in: {total}")
        '''elif api['endpoint'] == "/comics" and characters:
            names_comics_appear = set()
            for id, name in characters:
                print(id)
                print(name)
                total = get_all_values_comics(api,id)
                print(total)
                names_comics_appear.add((name,total))
            print(names_comics_appear)
        '''
    df = pd.DataFrame(characters_comics, columns=["id", "character_name", "quantity_comics"])

    df.to_csv("characters_comics.csv", index=False)
if __name__ == "__main__":
    main()