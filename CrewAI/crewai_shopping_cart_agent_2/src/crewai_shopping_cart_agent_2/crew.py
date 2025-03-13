from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
import os



# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class CrewaiShoppingCartAgent2():
	"""CrewaiShoppingCartAgent2 crew"""

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

	
	def manager_agent(self) -> Agent:		
		return Agent(
			
			verbose=False,
			max_rpm=1,
			max_iter=1,
			allow_delegation=True,
			llm=self.gemini_llm,
			role="Manager",
			goal= "Oversee the shopping process and delegate tasks.",
  			backstory= "A highly skilled AI designed to manage shopping workflows.",
  			 
  		
		)
	
	@agent
	def product_finder_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['product_finder_agent'],
			verbose=True,
			llm=self.gemini_llm,
			embedder=self.gemini_embedder_config, # adding embeder to the agent to get the context of the user query and 
												  # provide the answer in JSON format from knowledge base
			max_rpm=1,
			max_iter=1,
			allow_delegation=False,
			
		)
	
	 
	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	# @task
	# def manager_agent_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['manager_agent_task'],
	# 	)
	
	@task
	def product_finder_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['product_finder_agent_task'],
			output_file='report.md'
		)


	

	@crew
	def crew(self) -> Crew:
		"""Creates the CrewaiShoppingCartAgent2 crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		text_source = TextFileKnowledgeSource( file_paths=["inventory_rag_data.txt"] )

		print("self.agents = ",self.agents)


		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			process=Process.hierarchical,
			manager_agent=self.manager_agent(),
			
			#manager_llm=self.gemini_llm, # 
			knowledge_sources=[text_source],
			embedder=self.gemini_embedder_config,
		)
