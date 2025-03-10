import json


def parse_json(json_string, key):
     try:
        data = json.loads(json_string)
        if isinstance(data, dict) and key in data:
            return data[key]
        elif isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict) and key in v:
                    return v[key]
        return "Key not found"
     except json.JSONDecodeError as e:
        return "Invalid JSON string "+ str(e)
    
# This function returns the first key in the JSON object(laptop_dataset.txt)
# This function is used in the main.py file to get the model name from the JSON object
def get_model(json_string):
    try:
        data = json.loads(json_string)
        for key in data:
            return key
        return None  # Return None if the JSON object is empty
    except json.JSONDecodeError:
        return None # Return None for invalid JSON
    
# This function reads the contents of a file and returns the contents as a string
def read_inventory_file(file_path):
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
        return file_contents
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"

# Retrieve the collection for key e.g. "LAP001" from the JSON object returned by read_inventory_file  
def retrieve_inventory_record_by_id(json_string, key):
    try:
        data = json.loads(json_string)
        if isinstance(data, dict):
            if key in data:
                return data[key]
            else:
                return "Key not found in the collection"
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and key in item:
                    return item[key]
            return "Key not found in any item of the list"
        else:
            return "Invalid JSON format: Not a dictionary or a list"
    except json.JSONDecodeError:
        return "Invalid JSON string"