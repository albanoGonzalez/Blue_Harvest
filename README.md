# **MARVEL API - ALBANO GONZALEZ**

## **Purpose of the Assignment**

This project implements a data pipeline using the Marvel API to extract, transform, and load information about characters and their comic appearances. The goal is to provide a lightweight, extensible framework to interact with the API, process the data, and expose it via a FastAPI service for visualization and analysis.


---

# **MARVEL API - Data Integration and Visualization**

## **Project Overview**




## **What the Code Does**

### **1. API Configuration Management**
- The `mapping_apis.json` file provides metadata about each Api:
  - **base_url**: The url name.
  - **endpoint**: Endpoint to get the data
  - **params**: params to add in the call such as ts, public_key and private_key
 
With this json what I want to achieve is not to publish in my code any password or url in case they change. In aws I could configure it with the secrets manager or in azure I could do it too. I can also add the fields that I want to read from the json

---

### **2. Data Extraction from Marvel API**
- Here I read all the data from the API. To do this I need to create my account and get the keys to make API calls. Once I have them in the call I have to send a hash parameter with the combination of ts, public_key and private_key.
- To achieve this I call the endpoint /characters, I make multiple calls to get all the data. I keep the id and name field and create a list to store this. 
To make parallel API calls I could implement the multithreading part.

---

### **3. Data Transformation**
To get the total number of characters I will keep the name field we have in the json and for the total number of comics I will keep the available field. There is another endpoint /comics but it is not necessary to use it as the available field is enough. This way I am optimising time as retrieving all the data from the comics endpoint would take me more time.

- Get all the characters: from the endpoint the charcters I keep the name field to have all the names and save them in a list.
- Get quantity of comics: from the endpoint the charcters I keep the available field to have all the quantity of comes and save them in a list. 

--- I combine these two fields, also the id for each character and i save the tuple.


### **4. FastAPI**
- Depending if they want a csv file or write the values in an API I have created an API so they can see all the data, filter by the character names they want and see the total number of comics and also a chart with the 10 characters with the most comics.

### **5. Airflow**
- I have not had time to implement this part because I have been with a very important delivery that had to be deployed in prod in my work. Otherwise I would have liked to implement the etl in airflow to monitor the process so you can launch it daily.


### **6. Output Format**
- Writes the processed data to the `data folder` in **csv format**.
- I have chosen this format because it is easier to download and read, if it were to be stored I would have saved it in parquet format because it is better (Columnar storage, reducing storage requirements and High performance for both reading and writing)


### **Setup and Execution**

1. **Set Up the Environment**:
   - I have used pycharm as IDE
   - Clone the repository: https://github.com/albanoGonzalez/Blue_Harvest
   - install pyenv (if not already installed, to manage Python versions):
      - brew install pyenv
      - pyenv install 3.10.15
      - pyenv local 3.10.15
      - poetry env use $(pyenv which python)
   - In the repository folder run: "poetry install" to install the whole dependencies. If you have not already installed poetry you should do it before (curl -sSL https://install.python-poetry.org | python3)
   - poetry shell
   - set the interpreter in the IDE (the one you created, /.venv/bin/python/python3.10.15)
   


2. **Run the Script**:
   - Execute the script: `python main.py`.
   - Go to google and open the following url:  Endpoints: 
         - /data:  http://127.0.0.1:8000/data
         - /chart: http://127.0.0.1:8000/chart
         - /character-comics: http://127.0.0.1:8000/character-comics/?character_name=Karen%20Page

3. **Verify Output**:
   - Check the `data_folder` for csv file.


---

### **Future Improvements**
1. **Testing**:
   - Create some test to validate the code.
2. **Performance API CALL**: 
   - Implement multithreading.
3. **Integration with Cloud**:
   - Extend the pipeline to work directly with cloud storage (e.g., Azure Data Lake, AWS S3).
4. **Orchestration**:
   - Finish the implementation with Airflow
5. **Partitioning**:
   - If the file is very large we could partition it.
6. **DATABASE**:
   - Create a PostgreSQL database to store the data and run queries from there.

---


