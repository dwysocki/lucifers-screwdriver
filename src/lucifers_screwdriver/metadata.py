"""
Metadata processing utilities.
"""
import json as _json

def load(json_file):
    data = _json.load(json_file)

    return data
