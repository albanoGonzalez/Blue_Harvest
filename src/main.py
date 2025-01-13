from http.client import HTTPException

from Functions.connections import (
    load_json_config
)
from Functions.data import (
    get_all_values,
    get_names
)
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
import matplotlib.pyplot as plt
import os
import uvicorn

app = FastAPI()

DATA_PATH = "../data/characters_comics.csv"

#Endopoint to see the top 10 Characters by Comic Appearances
@app.get("/chart")
def generate_chart():
    """

    :return: chart to see the top 10 characters by quantity of comics
    """
    df = pd.read_csv(DATA_PATH)
    top_characters = df.nlargest(10, "quantity_comics")

    plt.figure(figsize=(10, 6))
    plt.bar(top_characters["character_name"], top_characters["quantity_comics"])
    plt.title("Top 10 Characters by Comic Appearances")
    plt.xlabel("Character Name")
    plt.ylabel("Number of Comics")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    chart_path = "top_characters_chart.png"
    plt.savefig(chart_path)
    plt.close()

    return FileResponse(chart_path, media_type="image/png")

#Endpoint to see the whole data
@app.get("/data")
def get_data():
    """

    :return: all the data in json format
    """
    if not os.path.exists(DATA_PATH):
        return {"error": "Data file not found"}
    df = pd.read_csv(DATA_PATH)
    return JSONResponse(content=df.to_dict(orient="records"))

#Endpoint to filter by any character
@app.get("/character-comics/")
def get_comics_by_character(character_name: str):
    """

    :param character_name: character name as an argument
    :return: quantity of comics for each character you filter by
    """
    try:
        df = pd.read_csv(DATA_PATH)

        character = df[df["character_name"].str.lower() == character_name.lower()]
        if character.empty:
            raise HTTPException(status_code=404, detail="Character not found")

        total_comics = int(character["quantity_comics"].iloc[0])
        return {"character_name": character_name, "total_comics": total_comics}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

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

    df.to_csv("../data/characters_comics.csv", index=False)
if __name__ == "__main__":
    main()
    uvicorn.run(app, host="127.0.0.1", port=8000)
