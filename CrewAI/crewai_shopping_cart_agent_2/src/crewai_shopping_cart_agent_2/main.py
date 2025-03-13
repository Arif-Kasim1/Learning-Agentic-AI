#!/usr/bin/env python
import sys
import warnings
import json
from crewai_shopping_cart_agent_2.util.utility import create_product_dict

from datetime import datetime
from crewai.flow import Flow, listen, start, router
from pydantic import BaseModel
from crewai_shopping_cart_agent_2.crew import CrewaiShoppingCartAgent2

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs',
        'current_year': str(datetime.now().year)
    }
    
    try:
        CrewaiShoppingCartAgent2().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

class OnlineShoppingState(BaseModel):
    shopping_cart: dict  = {}
    best_match: dict     = {}


class OnlineShoppingFlow(Flow[OnlineShoppingState]):

    @start()
    @listen("search_again")    
    def start_shopping_experiance(self):
        print("start_shopping_experiance")

        prefix = """product_finder_agent: find the same product and 3 other similer product like this,  
        """
        user_query = " NovaTech X1 Pro high-performance gaming laptop "

        result = (
            CrewaiShoppingCartAgent2()
            .crew()
            .kickoff(inputs={"user_query": prefix+user_query })
        )

        print("CrewaiShoppingCartAgent.start_shopping_experiance -> result = ", result.raw)
        
        product_detail = result.raw
        # product_detail = product_detail[product_detail.find('{') : product_detail.rfind('}')+1].strip()
        # product_detail = json.loads(product_detail) 

        # #iterate product_detail
        # for key, value in product_detail.items():
        #     print("key =  ", key, " | value = ",value)

        product_dict = create_product_dict(product_detail)

        print("-" * 50)
        print("\n\nproduct_dict = ", product_dict)

        # for key, value in product_dict.items():
        #     print("Key = ",key, " | Value = ", value) 

        for key in product_dict.keys():
            print("Key = ", key)

        for product_id, details in product_dict.items():
            print(f"Product ID: {details.get('product_id', 'N/A')}")
            print(f"Model Name: {details.get('model_name', 'N/A')}")
            print(f"Type: {details.get('type', 'N/A')}")
            print(f"Price: {details.get('price', 'N/A')}")
            print(f"Discount%: {details.get('discount', 'N/A')}")
            final_price = ""

            try:
                price = float(details.get('price', 'N/A'))
                discount = float(details.get('discount', 'N/A'))
                if discount < 0 or discount > 100:
                    break # handle invalid discount percentage
                final_price = price * (1 - discount / 100)
                 
            except (ValueError, TypeError):
                print("Error...")  # Handle invalid price or discount types
            
            print("Final Price: ", final_price)

            print("-" * 20) #separator
            


        # model_name = product_detail.get("model_name")
        # product_id = product_detail.get("product_id")
        # product_brand = product_detail.get("brand")
        # product_company = product_detail.get("company")
        # product_type = product_detail.get("type")
        # product_description = product_detail.get("description")
        # # in_stock = search_data.get("inventory").get("in_stock")
        # quantity = product_detail.get("quantity") 
        # price = product_detail.get("price") 
        # discount = product_detail.get("discount") 


        # print("model_name = ", model_name)
        # print("product_id = ", product_id)
        # print("product_brand = ", product_brand)
        # print("product_company = ", product_company)
        # print("product_type = ", product_type)
        # print("product_description = ", product_description)
        # # print("in_stock = ", in_stock)
        # print("quantity = ", quantity)
        # print("price = ", price)
        # print("discount = ", discount)





def kickoff():
    print("Starting OnlineShoppingFlow")
    shopping_cart_crew = OnlineShoppingFlow()
    print("shopping_cart_crew  = ", shopping_cart_crew )
    shopping_cart_crew.kickoff()