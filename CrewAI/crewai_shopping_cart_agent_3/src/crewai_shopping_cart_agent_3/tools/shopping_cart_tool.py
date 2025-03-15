from crewai.tools import tool


@tool("check_out_tool")
def check_out_tool(product_id: str) -> str:
    """check out tool is responsible to smothly check out 
    the customer shopping cart"""

    print("check_out_tool() called...product_id = ", product_id)

    return "Custom Check Out Tool: check out successfully..."

@tool("get_product_collection")
def get_product_collection() -> dict:
    """get product collection"""

    print("Get all product tool")

    product_collection = {
            1: '[product_id=LAP001,model_name=X1 Pro, company=TechNova, brand=NovaTech, type=Gaming Laptop, price=800, discount=5]',
            2: '[product_id=LAP004,model_name=Titan X17, company=GigaCore, brand=GigaTech, type=Gaming Laptop, price=1500, discount=10]',
            3: '[product_id=LAP007,model_name=Stealth X13, company=Velocity Systems, brand=Stealth, type=Gaming Laptop, price=1300, discount=9]',
            4: '[product_id=LAP009,model_name=Vortex 5X, company=StormTech, brand=Vortex, type=Gaming Laptop, price=1250, discount=7]' ,
        }

    return product_collection