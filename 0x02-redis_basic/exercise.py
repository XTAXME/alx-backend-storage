#!/usr/bin/env python3
"""
Cache class
"""


import redis
from uuid import uuid4
from functools import wraps
from typing import Union, Callable, Any


def count_calls(method: Callable) -> Callable:
    """Decorator to count calls to a function"""
    @wraps(method)
    def wrap_incr(self, *args, **kwargs) -> Any:
        """Wrap the method to count calls"""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrap_incr


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of calls to a function"""
    @wraps(method)
    def wrap_history(self, *args, **kwargs) -> Any:
        """Wrap the method to store the history of calls"""
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)
        self._redis.rpush(input_key, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(output_key, res)
        return res
    return wrap_history


def replay(method: Callable) -> None:
    """Decorator to replay the history of calls to a function"""
    redis_instance = method.__self__._redis
    input_key = "{}:inputs".format(method.__qualname__)
    output_key = "{}:outputs".format(method.__qualname__)

    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)
    print("{} was called {} times:".format(
        method.__qualname__,
        len(inputs)
    ))
    for in_args, out_args in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(
            method.__qualname__,
            in_args.decode("utf-8"),
            out_args
        ))


class Cache:
    """class cache"""
    def __init__(self) -> None:
        """initializes instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store data in cache"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Callable = None
            ) -> Union[str, bytes, int, float]:
        """get data from cache"""
        data = self._redis.get(key)
        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        """
        automatically parametrize Cache.get
        get data from cache
        """
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        automatically parametrize Cache.get
        get data from cache
        """
        return self.get(key, lambda x: int(x))
