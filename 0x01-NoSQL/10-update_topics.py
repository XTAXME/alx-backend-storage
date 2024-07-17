#!/usr/bin/env python3
""" Module updates many documents """
from typing import List


def update_topics(mongo_collection, name: str, topics: List[str]):
    """ Changes all topics of a school document based on the name """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
