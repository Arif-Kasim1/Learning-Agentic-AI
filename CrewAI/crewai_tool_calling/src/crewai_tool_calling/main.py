#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crewai_tool_calling.crew import CrewaiToolCalling

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
        'topic': 'what is the weather in New York?',
         
    }
    
    try:
        CrewaiToolCalling().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

