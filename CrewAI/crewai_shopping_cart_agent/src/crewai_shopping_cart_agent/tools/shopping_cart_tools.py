from crewai.tools import tool
from crewai_shopping_cart_agent.util.utility_function import read_inventory_file, retrieve_inventory_record_by_id


@tool("get_inventory_data")
def get_inventory_data(product_id: str) -> str:
    """read laptop inventory file and return the data by product_id."""
    print("TOOL (get_inventory_data): product_id = ", product_id)
    file_path = r"knowledge\laptop_inventory.txt"

    laptop_inventory: str = read_inventory_file(file_path)
    inventory_record = retrieve_inventory_record_by_id(laptop_inventory, product_id)

    # print("TOOL (get_inventory_data): laptop_inventory = ", laptop_inventory)
    # print("TOOL (get_inventory_data): inventory_record = ", inventory_record)

    return inventory_record




   