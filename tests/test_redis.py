"""
Examples from: https://redis.io/docs/clients/python/

These tests require redis to be running.
"""
import pytest
import redis


r = redis.Redis(host='localhost', port=6379, decode_responses=True)


import collections.abc

def _update_dict(d, u):
    """Utility for making updates to potentially nested dictionaries.

    Ideally json merge will take care of this for us when it becomes available in
    redis-py.
    """
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = _update_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d


class TestRedis():

    def test_string(self):
        r.delete("foo")
        resp = r.set("foo", "bar")
        assert resp == True
        resp = r.set("foo", "bar")
        assert resp == True
        assert r.get("foo") == "bar"
        r.delete("foo")

    def test_dict(self):
        k = "test-key:dict"
        d = {
            "name": "RedisUser",
            "age": 29
        }
        extra_field = "foo"
        resp = r.hdel(k, extra_field, *d.keys())
        assert resp in [0, len(d.keys()), len(d.keys())+1]
        resp = r.hset(k, mapping=d)
        assert resp == len(d.keys())
        d["age"] = str(d["age"]) # redis hashes only return strings
        assert r.hgetall(k) == d
        d[extra_field] = "bar"
        resp = r.hset(k, mapping=d)
        assert resp == 1 # we set 1 additional key
        assert r.hgetall(k) == d
        # cleanup
        r.hdel(k, extra_field, *d.keys())

    def test_json(self):
        """This does not seem to be supported yet? Or, maybe we need a schema?
        https://redis.io/docs/clients/python/
        """
        from redis.commands.json.path import Path
        k = "test-key:json"
        d = {
            "name": "RedisUser",
            "age": 29,
            "data": {
                "one": 1,
                "two": {
                    "three": 3,
                    "four": "four"
                }
            }
        }
        extra_field = "foo"
        resp = r.json().set(k, Path.root_path(), d)
        assert resp == True 
        obj = r.json().get(k)
        assert obj == d

        # Hopefully temporary approach to updates. Implementation of merge in redis-py
        # should eliminate the need for this. We could use paths instead, but this
        # does not provide a straightforward way of simply working with python dictionaries.
        updates = { "foo": "bar", "bat": "baz", "data": { "two": { "three": "three" } } }
        _update_dict(obj, updates) # do a deep update
        assert obj["foo"] == "bar"
        assert obj["name"] == "RedisUser"
        assert obj["age"] == 29
        assert obj["data"]["two"]["three"] == "three"
        assert obj["data"]["two"]["four"] == "four"
        resp = r.json().set(k, Path.root_path(), obj)
        assert resp == True
        updated_obj = r.json().get(k)
        assert updated_obj == obj

        # merge is not yet supported
        #d.update(updates)
        #resp = r.json().merge(k, Path.root_path(), updates)

        # cleanup
        r.json().delete(k)
