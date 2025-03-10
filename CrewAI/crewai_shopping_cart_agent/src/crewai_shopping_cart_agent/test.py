import json
from crewai_shopping_cart_agent.util.utility_function import read_inventory_file, retrieve_inventory_record_by_id, parse_json, get_model

def get_inventory_data(product_id: str) -> str:
    """read laptop inventory file and return the data by product_id."""
    # print("TOOL (get_inventory_data): product_id = ", product_id)
    file_path = r"knowledge\laptop_inventory.txt"

    laptop_inventory: str = read_inventory_file(file_path)
    inventory_record = retrieve_inventory_record_by_id(laptop_inventory, product_id)

    # print("TOOL (get_inventory_data): laptop_inventory = ", laptop_inventory)
    # print("TOOL (get_inventory_data): inventory_record = ", inventory_record)

    return inventory_record


inventory_data = get_inventory_data("LAP001") # Expected output: {'id': 'LAP001', 'brand': 'Lenovo', 'company': 'Lenovo', 'type': 'Workstation', 'description': 'Lenovo ThinkPad P15v Gen 1'}
# print("inventory_data = ", inventory_data)
# print(type(inventory_data))
#inventory_data = inventory_data[inventory_data.find('{') : inventory_data.rfind('}')+1].strip()

inventory_data = json.dumps( inventory_data ) 
# print("inventory_data = ", type(inventory_data))
inventory_data = json.loads(inventory_data) 


# print("get_inventory_data = ", inventory_data)



product_id = inventory_data.get("product_id")
model_name = inventory_data.get("model_name")
company = inventory_data.get("company")
brand = inventory_data.get("brand")
type = inventory_data.get("type")
description = inventory_data.get("description")
quantity = inventory_data.get("quantity")
price = inventory_data.get("price")
discount = inventory_data.get("discount")

print("product_id = ", product_id)
print("model_name = ", model_name)
print("company = ", company)
print("brand = ", brand)
print("type = ", type)
print("description = ", description)
print("quantity = ", quantity)
print("price = ", price)
print("discount = ", discount)


# raw =  '''{"product_id": "LAP001", "brand": "ThinkPad", 
# "company": "Lenovo", "type": "Workstation", 
# "description": "The Lenovo ThinkPad P15v is a powerful workstation designed for professionals. Equipped with high-performance processors, ample RAM, and a durable chassis, it ensures seamless multitasking and reliability. Its robust build, excellent keyboard, and security features make it ideal for engineers, developers, and business users needing top-tier performance.", "inventory": {"in_stock": true, "quantity": 43, "price": 800, "discount": 5}}'''
# inventory_data = json.loads(raw)

# print(type(inventory_data))
# print(inventory_data.get("product_id"))
# print(inventory_data.get("brand"))
# print(inventory_data.get("company"))
# print(inventory_data.get("type"))
# print(inventory_data.get("description"))
# print(inventory_data.get("inventory"))
# print(inventory_data.get("inventory").get("in_stock"))
# print(inventory_data.get("inventory").get("quantity"))
# print(inventory_data.get("inventory").get("price"))
# print(inventory_data.get("inventory").get("discount"))

# model_name = get_model(raw)
# product_id = parse_json(raw, "product_id")
# product_brand = parse_json(raw, "brand")
# product_company = parse_json(raw, "company")
# product_type = parse_json(raw, "type")
# product_description = parse_json(raw, "description")


# print("model_name = ", model_name)
# print("product_id = ", product_id)
# print("product_brand = ", product_brand)
# print("product_company = ", product_company)
# print("product_type = ", product_type)
# print("product_description = ", product_description)
