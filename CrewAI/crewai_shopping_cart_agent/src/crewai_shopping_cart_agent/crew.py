from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
import os
from crewai_shopping_cart_agent.tools.shopping_cart_tools import get_inventory_data

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class CrewaiShoppingCartAgent():
	"""CrewaiShoppingCartAgent crew"""

	GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
	gemini_llm = LLM(
    	model="gemini/gemini-1.5-flash",
    	api_key=GEMINI_API_KEY,
    	temperature=0,
	)

	gemini_embedder_config={
				"provider": "google",
				"config": {
					"model": "models/text-embedding-004",
					"api_key": GEMINI_API_KEY,
				}
			}


	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def manager_agent(self) -> Agent:
		
		return Agent(
			config=self.agents_config['manager_agent'],
			verbose=False,
			max_rpm=2,
			max_iter=2,
			allow_delegation=True,


		)

	@agent
	def customer_relationship_agent(self) -> Agent:
		
		return Agent(
			config=self.agents_config['customer_relationship_agent'],
			verbose=False,
			llm=self.gemini_llm,
			embedder=self.gemini_embedder_config, # adding embeder to the agent to get the context of the user query and 
												  # provide the answer in JSON format from knowledge base
			max_rpm=2,
			max_iter=2,
			
		)
	
	@agent
	def knowledge_rag_agent(self) -> Agent:
		
		return Agent(
			config=self.agents_config['knowledge_rag_agent'],
			verbose=False,
			llm=self.gemini_llm,
			embedder=self.gemini_embedder_config, # adding embeder to the agent to get the context of the user query and 
												  # provide the answer in JSON format from knowledge base
			max_rpm=2,
			max_iter=2,
			
		)
	

	
	@agent
	def inventory_agent(self) -> Agent:
			
		return Agent(
			config=self.agents_config['inventory_agent'],
			verbose=False,
			max_rpm=2,
			max_iter=2,
			tools=[get_inventory_data],
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def manager_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['manager_agent_task'],
		)

	@task
	def customer_relationship_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['customer_relationship_agent_task'],
			output_file='report.md'
		)
	
	@task
	def knowledge_rag_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['knowledge_rag_agent_task'],
			output_file='report.md'
		)
	
	@task
	def inventory_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['inventory_agent_task'],
			output_file='inventory_report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the CrewaiShoppingCartAgent crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		text_source = TextFileKnowledgeSource( file_paths=["inventory_rag_data.txt"] )
		#print("text_source.content: ", text_source.content)

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			#process=Process.sequential,
			verbose=False,
			process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			#manager_agent=self.manager_agent,
			manager_llm=self.gemini_llm,
			knowledge_sources=[text_source],
			embedder=self.gemini_embedder_config,
		)
