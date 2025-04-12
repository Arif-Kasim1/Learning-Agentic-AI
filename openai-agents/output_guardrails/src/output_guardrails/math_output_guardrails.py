from __future__ import annotations

import asyncio
import json

from pydantic import BaseModel, Field

from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    output_guardrail,
)
from LLMConfig import model, config


class MessageOutput(BaseModel):
    response: str

class MathOutput(BaseModel):
    is_math: bool
    reasoning: str

guardrail_agent2 = Agent(
    name="Guardrail check",
    instructions="Check if the output includes any math.",
    output_type=MathOutput,
)

@output_guardrail 
async def math_guardrail2(
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent2, output.response, context=ctx.context, run_config = config)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math,
    )


agent2 = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    output_guardrails=[math_guardrail2],
    output_type=MessageOutput,
)

async def main():
    # This should trip the guardrail
    question: str = input("Enter a math question: ")
    try:
        response = await Runner.run(agent2, question, run_config = config)
        print("Guardrail didn't trip - this is unexpected")
        print("Response:", response.final_output.response)

    except OutputGuardrailTripwireTriggered:
        print("Math output guardrail tripped")

if __name__ == "__main__":
    asyncio.run(main())