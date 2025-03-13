import json

def create_product_dict(json_data_string):
    #Helper function to convert a string to a dictionary
    def string_to_dict(input_string):
        # Find start and end indices of the JSON object within the string
        start_index = input_string.find('{')
        end_index = input_string.rfind('}')
        
        if start_index == -1 or end_index == -1:
            return None  # Or handle the error appropriately
        
        # Extract the substring containing the JSON object
        json_substring = input_string[start_index : end_index+1]
        
        try:
          # Attempt to parse the JSON substring
          return json.loads(json_substring)
        except json.JSONDecodeError as e:
          print("JSONDecodeError: ", e)
          return None

    product_dict = {}
    data = string_to_dict(json_data_string)

    if data:
        for product_id, details in data.items():
            product_dict[details.get('product_id', "")] = details
    
        return product_dict
    else:
        return "Invalid JSON data"
