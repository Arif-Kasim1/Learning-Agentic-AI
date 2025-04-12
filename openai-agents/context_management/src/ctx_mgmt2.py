import asyncio
from dataclasses import dataclass

from agents import Agent, RunContextWrapper, Runner, function_tool
from LLMConfig import model


@dataclass
class UserInfo:
    name: str
    uid: int

@function_tool
async def greet_user(context: RunContextWrapper[UserInfo], greeting: str) -> str:
  """Greets the User with their name.
  Args:
    greeting: A specialed greeting message for user
  """
  name = context.context.name
  uid = context.context.uid
  return f"Hello {name}, ({uid}), {greeting} Pakistan chapter"

async def main():
    user_info = UserInfo(name="Arif Rozani", uid=123)

    agent = Agent[UserInfo](
        name="Assistant",
        tools=[greet_user],
        model=model,
        instructions="Always greet the user using <function_call>greet_user</function_call> and welcome them to Panaversity"
    )

    result = await Runner.run(
        starting_agent=agent,
        input="Hi, Arif is from which country?",
        context=user_info,
    )

    print(result.final_output)

asyncio.run(main())