#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from crewai_shopping_cart_agent.crew import CrewaiShoppingCartAgent
from crewai.flow import Flow, listen, start, router
from pydantic import BaseModel
from util.utility_function import parse_json, get_model

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information



class OnlineShoppingState(BaseModel):
    shopping_cart: list  = []
    best_match: list     = []



class OnlineShoppingFlow(Flow[OnlineShoppingState]):
    
    @listen("search_again")
    @start()
    def start_shopping_experiance(self):
        print("Welcome to the online laptop store")
        pre_fix = "delegate this task to  sales_agent so it can serch from knowledge base and answer in JSON format: "
        user_query = input("what type of laptop are you looking for?")
        result = (
            CrewaiShoppingCartAgent()
            .crew()
            .kickoff(inputs={"user_query": pre_fix+user_query})
        )
        print("CrewaiShoppingCartAgent -> result.raw = ", result.raw)

        model_name = get_model(result.raw)
        product_id = parse_json(result.raw, "id")
        product_brand = parse_json(result.raw, "brand")
        product_company = parse_json(result.raw, "company")
        product_type = parse_json(result.raw, "type")
        product_description = parse_json(result.raw, "description")

        print("model_name = ", model_name)
        print("product_id = ", product_id)
        print("product_brand = ", product_brand)
        print("product_company = ", product_company)
        print("product_type = ", product_type)
        print("product_description = ", product_description)




        result = ["best match", "second best match", "third best match"]
        self.state.best_match = result

        

    
    @router(start_shopping_experiance)
    def search_results(self):
        print("Here are the search results")
        for i in range(len(self.state.best_match)):
            print(f"Item #: {i+1},  {self.state.best_match[i]}")
        print("Itme #: 4, Search again")    
      

        user_choice = input("Which item # would you like to add to cart?")
        if user_choice.isdigit() and int(user_choice) <= len(self.state.best_match):
            self.state.shopping_cart.append(self.state.best_match[int(user_choice)-1] )
            print("Item added to cart")
        else:
            print("Item not added to cart")
            return "search_again"

        print("Here is your current cart status", self.state.shopping_cart)

        return "checkout"


    @listen("checkout")
    def checkout1(self):
        print("You are now checking out")
        print("Here is your cart", self.state.shopping_cart)
        print("Thank you for shopping with us")

        self.state.shopping_cart = []  # reset the state
        self.state.best_match    = []  # reset the state

         


def kickoff():
    print("Starting OnlineShoppingFlow")
    shopping_cart_crew = OnlineShoppingFlow()
    print("shopping_cart_crew  = ", shopping_cart_crew )
    shopping_cart_crew.kickoff()