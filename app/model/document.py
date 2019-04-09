# Related
import mongoengine as me

class Metadata(me.DynamicEmbeddedDocument):
    dataset = me.StringField(required=True)
    sample_id = me.IntField(required=True)
    file_id = me.IntField(required=True)
    instrument = me.StringField(required=True)  
    meta = { "indexes": ["sample_id", 
                        "file_id"
                        ] 
        }  

class Sample(me.DynamicDocument):
    class Meta:
        collection = "default"

    metadata = me.EmbeddedDocumentField(Metadata)
    meta = { "indexes": ["metadata.sample_id", 
                        "metadata.file_id"
                        ] 
        }