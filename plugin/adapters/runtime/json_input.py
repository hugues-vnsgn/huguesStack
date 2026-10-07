"""Bounded JSON inputs: ambiguous objects and excessive nesting hold."""
import json


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key: ' + key)
        result[key] = value
    return result


def load_json(text):
    try:
        value = json.loads(text, object_pairs_hook=_unique_object)
    except RecursionError as exc:
        raise ValueError('JSON nesting exceeds supported depth') from exc
    pending = [(value, 0)]
    while pending:
        child, depth = pending.pop()
        if depth > 64:
            raise ValueError('JSON nesting exceeds supported depth')
        if isinstance(child, dict):
            pending.extend((item, depth + 1) for item in child.values())
        elif isinstance(child, list):
            pending.extend((item, depth + 1) for item in child)
    return value
