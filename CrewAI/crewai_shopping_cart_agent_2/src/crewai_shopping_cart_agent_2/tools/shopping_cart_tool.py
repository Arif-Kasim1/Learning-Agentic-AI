from crewai.tools import tool


@tool("check_out_tool")
def check_out_tool(product_id: str) -> str:
    """check out tool is responsible to smothly check out 
    the customer shopping cart"""

    print("check_out_tool() called...product_id = ", product_id)

    return "Custom Check Out Tool: check out successfully..."