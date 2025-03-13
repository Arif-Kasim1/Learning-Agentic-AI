#!/usr/bin/env python
import json
import sys
import warnings
from datetime import datetime
from crewai_shopping_cart_agent.crew import CrewaiShoppingCartAgent
from crewai.flow import Flow, listen, start, router
from pydantic import BaseModel
from crewai_shopping_cart_agent.util.utility_function import parse_json, get_model

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information



class OnlineShoppingState(BaseModel):
    shopping_cart: dict  = {}
    best_match: dict     = {}



class OnlineShoppingFlow(Flow[OnlineShoppingState]):
    
    
    def front_desk(self):
        
        print("Welcome to Global Business Machine! How may I help you?")
        prefix = "delegate this task to Customer Relationship Agent so it can answer the user query using knowledge base RAG  " 
        input_query = input("User: ") 

        result = ""

        while input_query != "exit":
            result = (
                CrewaiShoppingCartAgent()
                .crew()
                .kickoff(inputs={"user_query": prefix+input_query, "product_id": "product_id" })
            )
            print("Bot: ", result.raw)
            input_query = input("User: ")

        
    def get_product_id(self):
        print("Getting the product id")
        #user_query = input("What type of laptop are you looking for? ")
        user_query = "NovaTech X1 Pro high-performance gaming laptop "
        print("User query = ", user_query)

        prefix = f"delegate to knowledge_rag_agent to find the from rag knowledge {user_query}"
        result = (
            CrewaiShoppingCartAgent()
            .crew()
            .kickoff(inputs={"user_query": prefix+user_query, "product_id": "product_id" })
        )
        print("CrewaiShoppingCartAgent.start_shopping_experiance -> result = ", result.raw)


        return user_query    

    @start()
    @listen("search_again")    
    def start_shopping_experiance(self):
        print("start_shopping_experiance")

        prefix = "delegate this task to  Inventory Agent so it can search, model_name, product_id, brand, company, " \
        "type and description, price, quantity, discount using tool " \
        " and answer in JSON format " \
         
        #input("what type of laptop are you looking for?", "i would like to buy lenovo p15v workstation")
        user_query = "NovaTech X1 Pro, gaming laptop by TechNova"

        print("Calling the CrewaiShoppingCartAgent with query = ", prefix+user_query)
        result = (
            CrewaiShoppingCartAgent()
            .crew()
            .kickoff(inputs={"user_query": prefix+user_query, "product_id": "product_id" })
        )
        print("CrewaiShoppingCartAgent.start_shopping_experiance -> result = ", result.raw)
        #product_detail = json.loads(result.raw)

        product_detail = result.raw
        print("product_detail = ", type(product_detail))

        # product_detail = product_detail.removeprefix("```json\n")
        # product_detail = product_detail.removesuffix("   \n```")
        # print("product_detail = ", product_detail)

        # product_detail =  dict(product_detail)  

        product_detail = product_detail[product_detail.find('{') : product_detail.rfind('}')+1].strip()

        product_detail = json.loads(product_detail) 

        # search_data = json.loads(result.raw)
        model_name = product_detail.get("model_name")
        product_id = product_detail.get("product_id")
        product_brand = product_detail.get("brand")
        product_company = product_detail.get("company")
        product_type = product_detail.get("type")
        product_description = product_detail.get("description")
        # in_stock = search_data.get("inventory").get("in_stock")
        quantity = product_detail.get("quantity") 
        price = product_detail.get("price") 
        discount = product_detail.get("discount") 

        # model_name = product_detail.get("model_name")
        # product_id = product_detail.get("product_id")
        # product_brand = product_detail.get("product_brand")
        # product_company = product_detail.get("product_company")
        # product_type = product_detail.get("product_type")
        # product_description = product_detail.get("product_description")


        print("model_name = ", model_name)
        print("product_id = ", product_id)
        print("product_brand = ", product_brand)
        print("product_company = ", product_company)
        print("product_type = ", product_type)
        print("product_description = ", product_description)
        # print("in_stock = ", in_stock)
        print("quantity = ", quantity)
        print("price = ", price)
        print("discount = ", discount)





        #result = ["best match", "second best match", "third best match"]
        self.state.best_match['product_detail'] = product_detail


    @listen("start_shopping_experiance")
    def get_inventory_data(self):
        print("Getting inventory data")

        # product_detail = self.state.best_match['product_detail']
        # product_id = product_detail.get("product_id")

        # user_query = f"get the inventory detail for product_id={product_id} from Inventory Agent using tool get_inventory_data"

        # result = (
        #     CrewaiShoppingCartAgent()
        #     .crew()
        #     .kickoff(inputs={"user_query":  user_query, "product_id": product_id })
        # )
        # print("CrewaiShoppingCartAgent.get_inventory_data -> result = ", result.raw)

        # inventory_data = result.raw
        
        # #product_detail = product_detail[product_detail.find('{') : product_detail.rfind('}')+1].strip()
        # inventory_data = inventory_data[inventory_data.find('{') : inventory_data.rfind('}')+1].strip()
        # print("inventory_data = ", inventory_data)

        # inventory_data = json.loads(inventory_data)

        # product_id = inventory_data.get("product_id")
        # quantity = inventory_data.get("quantity")
        # price = inventory_data.get("price")
        # discount = inventory_data.get("discount")

        # print("product_id = ", product_id)
        # print("quantity = ", quantity)
        # print("price = ", price)
        # print("discount = ", discount)

        # self.state.best_match['inventory_data'] = inventory_data



        
    
    @router(get_inventory_data)
    def search_results(self):
        print("Here are the search results")

        # for loop to print self.state.best_match key value pairs
        for key, value in self.state.best_match.items():
            print(f"key = {key}: value = {value}")

        # for i in range(len(self.state.best_match)):
        #     print(f"Item #: {i+1},  {self.state.best_match[i]}")
        # print("Itme #: 4, Search again")    
      
        product_detail = self.state.best_match['product_detail']
        #inventory_data = self.state.best_match['inventory_data']    

        print("product_detail = ", product_detail)

        print("price = ", product_detail.get("price"))  
        print("We have a discount of ", product_detail.get("discount"), "%")
        print("The final price is ", product_detail.get("price") - product_detail.get("price") * product_detail.get("discount")/100)




        user_choice = input("Which item # would you like to add to cart? yes | no | exit : ")
        if user_choice == "yes":  
            self.state.shopping_cart['item'+str(len(self.state.shopping_cart)+1)] = {"product_detail":product_detail}
            print("Item added to cart successfully = ", self.state.shopping_cart)
        elif user_choice == "no":
            print("Item not added to cart")
            return "search_again"
        elif user_choice == "exit":
            print("Exiting the shopping experiance")
            return "exit"

        print("Here is your current cart status", self.state.shopping_cart)

        return "checkout_user"


    @listen("checkout_user")
    def checkout(self):
        print("You are now checking out")
        print("Here is your cart", self.state.shopping_cart)
        print("Thank you for shopping with us")

        self.state.shopping_cart = {}  # reset the state
        self.state.best_match    = {}  # reset the state

    @listen("exit")
    def checkout1(self):
        print("You are now exiting the shopping experiance")
        
        print("Thank you for shopping with us")

        self.state.shopping_cart = {}  # reset the state
        self.state.best_match    = {}  # reset the state   
        print("Here is your cart", self.state.shopping_cart) 


def kickoff():
    print("Starting OnlineShoppingFlow")
    shopping_cart_crew = OnlineShoppingFlow()
    print("shopping_cart_crew  = ", shopping_cart_crew )
    shopping_cart_crew.kickoff()