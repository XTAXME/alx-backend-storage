#!/usr/bin/env python3
""" Module inserts a document """
from bson.objectid import ObjectId


def insert_school(mongo_collection, **kwargs) -> ObjectId:
    """ Inserts a new document in a collection based on kwargs """
    inserted_doc = mongo_collection.insert_one(kwargs)
    return inserted_doc.inserted_id
