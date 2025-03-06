from crewai import Agent, Task, Crew
from openai import OpenAI
from google import genai
import os

#genai.Client(api_key=os.environ['GEMINI_API_KEY'])

# Initialize LLM (Gemini or OpenAI API as placeholder)
#llm = genai.GenerativeModel(model_name='gemini-1.5-flash')
llm = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

def llm_query(prompt):
    response = llm.models.generate_content(model='gemini-2.0-flash', 
                                           contents=prompt)
    return response["generated_text"].strip()


# Product Catalog Agent
class ProductCatalog:
    def __init__(self):
        self.products = {
            "laptop": {"name": "Laptop", "price": 1000, "stock": 10},
            "phone": {"name": "Smartphone", "price": 500, "stock": 20}
        }
    
    def search_product(self, product_name):
        return self.products.get(product_name.lower(), None)

product_catalog = ProductCatalog()

product_agent = Agent(
    name="Product Catalog Agent",
    role="Handles product details and searches for items",
    tools={"search_product": product_catalog.search_product}
)

# Shopping Cart Agent
class ShoppingCart:
    def __init__(self):
        self.cart = []
    
    def add_to_cart(self, product):
        self.cart.append(product)
        return f"{product['name']} added to cart."
    
    def checkout(self):
        return f"Checked out {len(self.cart)} items."

shopping_cart = ShoppingCart()

cart_agent = Agent(
    name="Shopping Cart Agent",
    role="Manages shopping cart and checkout",
    tools={
        "add_to_cart": shopping_cart.add_to_cart,
        "checkout": shopping_cart.checkout
    }
)

# Shopping Orchestration Agent
class ShoppingOrchestration:
    def __init__(self, product_agent, cart_agent):
        self.product_agent = product_agent
        self.cart_agent = cart_agent
    
    def process_order(self, user_query):
        product_name = llm_query(f"Extract product from user request: {user_query}")
        product = self.product_agent.tools["search_product"](product_name)
        if product:
            response = self.cart_agent.tools["add_to_cart"](product)
            return response
        return "Product not found."

orchestration = ShoppingOrchestration(product_agent, cart_agent)

orchestration_agent = Agent(
    name="Shopping Orchestration Agent",
    role="Coordinates shopping process autonomously",
    tools={"process_order": orchestration.process_order}
)

# Tasks with Autonomy
product_search_task = Task("Find product details", agent=product_agent, async_execution=True)
add_to_cart_task = Task("Add product to cart", agent=cart_agent, async_execution=True)
checkout_task = Task("Checkout items in cart", agent=cart_agent, async_execution=True)

# Crew with Parallel Execution
crew = Crew(agents=[orchestration_agent, product_agent, cart_agent], tasks=[product_search_task, add_to_cart_task, checkout_task], parallel_execution=True)

# Example Usage
print("Product Search Task:")
print(orchestration.process_order("I need a new laptop for gaming."))
