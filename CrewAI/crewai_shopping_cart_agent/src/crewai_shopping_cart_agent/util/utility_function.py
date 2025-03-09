import json


def parse_json(json_string, key):
    try:
        data = json.loads(json_string)
        for outer_key, value in data.items():
            if isinstance(value, dict):
                if key in value:
                    return value[key]
        return "Key not found"
    except json.JSONDecodeError:
        return "Invalid JSON string"
    

def get_model(json_string):
    try:
        data = json.loads(json_string)
        for key in data:
            return key
        return None  # Return None if the JSON object is empty
    except json.JSONDecodeError:
        return None # Return None for invalid JSON