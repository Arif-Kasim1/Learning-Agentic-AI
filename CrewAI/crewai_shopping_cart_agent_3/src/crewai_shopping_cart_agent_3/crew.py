from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
import os
from crewai_shopping_cart_agent_3.tools.shopping_cart_tool import check_out_tool, get_product_collection




# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class CrewaiShoppingCartAgent3():
	"""CrewaiShoppingCartAgent3 crew"""

	GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
	gemini_llm = LLM(
		model="gemini/gemini-1.5-flash", #gemini-1.5-flash gemini-2.0-flash-exp
		api_key=GEMINI_API_KEY,
		temperature=0,
	)

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools

	def manager_agent(self) -> Agent:		
		return Agent(
			
			verbose=True,
			max_rpm=10,
			max_iter=10,
			allow_delegation=True,
			llm=self.gemini_llm,
			role="Manager",
			goal= """Oversee the shopping process and delegate tasks to appropriate agent. dont do any search or use tool by your own.
			 		 you are just orchestrating the process""",
  			backstory= "A highly skilled to manage shopping workflows.",  		
		)
	

	@agent
	def product_finder_agent(self) -> Agent:
		"""product_finder_agent responsible to find information from Knowledge"""
		return Agent(
			config=self.agents_config['product_finder_agent'],
			verbose=True,
			llm=self.gemini_llm,
			# embedder=self.gemini_embedder_config, # adding embeder to the agent to get the context of the user query and 
			# 									  # provide the answer in JSON format from knowledge base
			max_rpm=10,
			max_iter=10,
			allow_delegation=False,	
			tools=[get_product_collection]		
		)
	
	# @agent
	# def check_out_agent(self) -> Agent:
	# 	"""check_out_agent is responsible for check out process with the provided tools"""
	# 	return Agent(
	# 		config=self.agents_config['check_out_agent'],
	# 		verbose=True,
	# 		llm=self.gemini_llm,			
	# 		max_rpm=10,
	# 		max_iter=10,
	# 		allow_delegation=False,
	# 		tools=[check_out_tool]			
	# 	)

 
	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task


		
	@task
	def product_finder_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['product_finder_agent_task'],
			output_file='report.md'
		)
	
	# @task
	# def check_out_agent_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['check_out_agent_task'],
	# 		output_file='check_out.md'
	# 	)
	

 

	@crew
	def crew(self) -> Crew:
		"""Creates the CrewaiShoppingCartAgent2 crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		#text_source = TextFileKnowledgeSource( file_paths=["inventory_rag_data.txt"] )

		print("self.agents = ",self.agents)


		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			process=Process.hierarchical,
			manager_agent=self.manager_agent(),
			
			#manager_llm=self.gemini_llm, # 
			#knowledge_sources=[text_source],
			#embedder=self.gemini_embedder_config,
		)
