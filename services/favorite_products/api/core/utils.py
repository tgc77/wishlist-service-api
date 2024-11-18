from datetime import date
import json
import decimal
from typing import Dict
import uuid

from pydantic import BaseModel


def ipdb_set_trace():
    import ipdb
    return ipdb.set_trace()


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


def get_json_pydantic_model(entity: BaseModel) -> Dict:
    if entity is None:
        return {}
    entity_data = json.dumps(entity.model_dump(), cls=CustomJSONEncoder)
    entity_json = json.loads(entity_data)
    return entity_json
