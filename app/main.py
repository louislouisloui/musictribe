# Native
import datetime
# Related
import pprint
from pymongo import MongoClient
# Local
from rsc.databuilder import DataBuilder
from rsc.inserter import Inserter
from mongoengine import connect

if __name__ == "__main__":
    # Clean the DB
    client = MongoClient("mongodb://mongo:27017")
    for db in client.list_database_names():
        for collection in client[db].list_collection_names():
            try:
                client[db].drop_collection(collection)
            except Exception as e:
                print(e)
    client.close()
    # Extraction/Insertion
    print("Extracting JSONs")
    timer = datetime.datetime.now()
    databuilder = DataBuilder()
    data_dir = "data"
    samples = databuilder.load(data_dir)
    print(f"Extracted all JSONs ({((datetime.datetime.now()-timer).seconds)}s)")
    print("Inserting in Mongo")
    timer = datetime.datetime.now()
    inserter = Inserter()
    inserter.insert(samples)
    print(f"Inserted all JSONs ({((datetime.datetime.now()-timer).seconds)}s)")
    

    
