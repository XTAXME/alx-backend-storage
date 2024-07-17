#!/usr/bin/env python3
""" Module lists all documents in a collection """
from typing import List


def list_all(mongo_collection) -> List[dict]:
    """ Return empty list if no document in the collection  """
    return list(mongo_collection.find())
