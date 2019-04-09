# Native
import datetime
# Related
from mongoengine import connect, register_connection
from mongoengine.context_managers import switch_collection, switch_db
# Local
from model.schema import make_schema
from rsc.helpers import sort_data_between
from model.document import Sample
from marshmallow import INCLUDE

class Inserter():
    def __init__(self, mongo_uri="mongodb://mongo:27017"):
        self.mongo_uri = mongo_uri
        self._connect(self.mongo_uri)
        self.sample = Sample

    def _connect(self,uri):
        connect(host=uri)

    def insert(self,datas):
        self._insert_in_db(datas)

    def _insert_in_db(self,datas):
        db_samples = sort_data_between(datas, "dataset")
        for db,samples in db_samples.items():
            register_connection(db,db, host = self.mongo_uri)
            with switch_db(self.sample, db) as Sample:
                print(f">> Inserting in DB {db}")
                timer = datetime.datetime.now()
                self._insert_in_collection(samples, Sample)
                print(f">> Inserted {len(samples)} documents in DB {db} ({(datetime.datetime.now()-timer).total_seconds()}s)")
                # Improve to return error count

    def _insert_in_collection(self, datas, sample_class):
        collections_samples = sort_data_between(datas, "instrument")
        for collection,samples in collections_samples.items():
            with switch_collection(sample_class, collection) as Sample:
                timer = datetime.datetime.now()
                for sample in samples:
                    self._insert_one(sample, Sample)
                print(f">>>> Inserted {len(samples)} documents in collection {collection} ({(datetime.datetime.now()-timer).seconds}s)")

    def _insert_one(self, data, doc_context):
        # Improve to handle errors (retry, logging)
        doc = self._get_doc(data, doc_context)
        try:
            doc.save()
        except Exception as e:
            print(e)
    
    def _get_doc(self, doc, doc_context):
        schema = make_schema(doc_context)
        try:
            return schema().load(doc)
        except Exception as err:
            print(f"Load exception: {err}")

    