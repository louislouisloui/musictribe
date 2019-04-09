# Native
import datetime
# Related
import marshmallow_mongoengine as ma
from marshmallow.decorators import pre_load
from marshmallow.fields import Nested
from marshmallow import INCLUDE
# Local
from model.document import Metadata

class MetadataSchema(ma.ModelSchema):
    class Meta:
        model = Metadata
        unknown = INCLUDE

def make_schema(instrument):
    class InstrumentSchema(ma.ModelSchema):
        class Meta:
            model = instrument
            unknown = INCLUDE
        metadata = Nested(MetadataSchema)
        @pre_load
        def add_insert_ts(self,data):
            data.setdefault("insert_time",datetime.datetime.now().isoformat())
            return data
    return InstrumentSchema