#!/usr/bin/env python3
""" Log stats module"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    log_collection = client.logs.nginx

    docs_count = log_collection.count_documents({})
    print(f"{docs_count} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    for method in methods:
        count = log_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    status = log_collection.count_documents({
        "$and": [
            {"method": "GET"},
            {"path": "/status"}
        ]
    })
    print(f'{status} status check')
