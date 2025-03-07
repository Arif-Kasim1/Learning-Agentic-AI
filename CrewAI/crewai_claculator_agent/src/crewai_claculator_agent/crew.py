from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os

from crewai import Crew, Process
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
# from crewai.memory.storage import LTMSQLiteStorage, RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory.storage.rag_storage import RAGStorage

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class CrewaiClaculatorAgent():
	"""CrewaiClaculatorAgent crew"""

	GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
	gemini_llm = LLM(
    	model="gemini/gemini-1.5-flash",
    	api_key=GEMINI_API_KEY,
    	temperature=0,
	)

	os.environ['CREWAI_STORAGE_DIR']='/crew_memory'

	google_embedder = {
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
	def calculator_orchestrator_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['calculator_orchestrator_agent'],
			verbose=True,
			llm=self.gemini_llm
		)

	@agent
	def addition_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['addition_agent'],
			verbose=True,
			llm=self.gemini_llm
		)
	
	@agent
	def subtraction_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['subtraction_agent'],
			verbose=True,
			llm=self.gemini_llm
		)

	@agent
	def multiplication_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['multiplication_agent'],
			verbose=True,
			llm=self.gemini_llm
		)
	
	@agent
	def division_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['division_agent'],
			verbose=True,
			llm=self.gemini_llm
		)
	

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def calculator_orchestrator_task(self) -> Task:
		return Task(
			config=self.tasks_config['orchestrate_calculation'],
		)

	@task
	def addition_task(self) -> Task:
		return Task(
			config=self.tasks_config['perform_addition'],
			output_file='/reports/report.md'
		)

	@task
	def subtraction_task(self) -> Task:
		return Task(
			config=self.tasks_config['perform_subtraction'],
			output_file='report.md'
		)
	
	@task
	def multiplication_task(self) -> Task:
		return Task(
			config=self.tasks_config['perform_multiplication'],
			output_file='report.md'
		)

	@task
	def division_task(self) -> Task:
		return Task(
			config=self.tasks_config['perform_division'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the CrewaiClaculatorAgent crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			#process=Process.sequential,
			
			verbose=True,
			planning=True,
			planning_llm=self.gemini_llm,
			#process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			#manager_llm=self.gemini_llm,
			# Enable long-term memory for the crew
			memory = True,
			# Long-term memory for persistent storage across sessions
			long_term_memory = LongTermMemory(
				storage=LTMSQLiteStorage(
					db_path="./my_crew2/long_term_memory_storage1.db"
				)
			),
			# Short-term memory for current context using RAG
			short_term_memory = ShortTermMemory(
				storage = RAGStorage(
						embedder_config=self.google_embedder,
						type="short_term",
						path="./my_crew2/short_term1/"
					)
				),

			# Entity memory for tracking key information about entities
			entity_memory = EntityMemory(
				storage=RAGStorage(
					embedder_config=self.google_embedder,
					type="short_term",
					path="./my_crew2/entity1/"
				)
			),
		)
