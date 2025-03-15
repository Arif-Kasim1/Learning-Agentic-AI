#!/usr/bin/env python
import sys
import warnings
import json
from crewai_shopping_cart_agent_3.util.utility import create_product_dict
from crewai_shopping_cart_agent_3.util.utility import get_line_by_number

from datetime import datetime
from crewai.flow import Flow, listen, start, router
from pydantic import BaseModel
from crewai_shopping_cart_agent_3.crew import CrewaiShoppingCartAgent3

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
        CrewaiShoppingCartAgent3().crew().kickoff(inputs=inputs)
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

        prefix = """delegate task to Product Finder Agent,  
        """
        user_query = " NovaTech X1 Pro high-performance gaming laptop "

        result = (
            CrewaiShoppingCartAgent3()
            .crew()
            .kickoff(inputs={"user_query": prefix+user_query })
        )

        product_detail = result.raw
        print("CrewaiShoppingCartAgent.start_shopping_experiance -> result = \n", product_detail)
         
        self.state.best_match['product_detail'] = product_detail

       
    @router(start_shopping_experiance)
    def customer_decision(self):
        print("customer_decision")
        print("Input 0 to search again, to exit type x.")
        decision = input("Type your desired product_id to be added in cart: ")

        if decision == "0":  
            print("search_again")          
            return "search_again"
        elif decision == "x":
            print("Now exiting...")
            sys.exit()
        else:
            item_number: int = int(decision)   
            product_detail = self.state.best_match.get('product_detail')        
            self.state.shopping_cart['Item 01'] =  get_line_by_number(product_detail, item_number)
            print('Item 01 in Shopping Cart = ', self.state.shopping_cart.get('Item 01'))

            return "check_out"


    @listen("check_out")
    def customer_check_out(self):

        print("Customer check out...")

        # prefix = """Agent=Check Out Agent,  """
        # user_query = " call the Check Out Agent "

        # result = (
        #     CrewaiShoppingCartAgent2()
        #     .crew()
        #     .kickoff(inputs={"user_query": prefix+user_query })
        # )

        # print("customer_check_out: result.raw = ", result.raw)

       


def kickoff():
    print("Starting OnlineShoppingFlow")
    shopping_cart_crew = OnlineShoppingFlow()
    print("shopping_cart_crew  = ", shopping_cart_crew )
    shopping_cart_crew.kickoff()