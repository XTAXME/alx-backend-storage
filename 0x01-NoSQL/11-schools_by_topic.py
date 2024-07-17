#!/usr/bin/env python3
""" Module returns list of schools based on topic """

def schools_by_topic(mongo_collection, topic):
    """ Return list of school having a specific topic """
    school_lst = list(mongo_collection.find({ "topics": topic }))
    return school_lst
