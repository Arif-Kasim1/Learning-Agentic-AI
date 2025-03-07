#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crewai_unit_converter.crew import CrewaiUnitConverter

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    user_input = sys.argv[1] if len(sys.argv) > 1 else None
    print(f"User input: {user_input}")  # This is just an example, you can remove this line

  
    user_input = input("Enter NLP for unit Conversion: ") if user_input is None else user_input


    inputs = {         
        'user_input': user_input,
    }
    
    try:
        CrewaiUnitConverter().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


