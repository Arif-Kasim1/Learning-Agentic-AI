#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crewai_claculator_agent.crew import CrewaiClaculatorAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    print("Welcome to the CrewAI Calculator Agent") 

    calculation  = input("Enter the arthimatic calculation(+-/*): ")

    inputs = {
        'calculation': calculation
        
    }
    
    try:
        CrewaiClaculatorAgent().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


