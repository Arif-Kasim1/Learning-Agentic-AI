import asyncio
from dataclasses import dataclass

from agents import Agent, RunContextWrapper, Runner, function_tool
from LLMConfig import model


@dataclass
class UserInfo:  
    name: str
    uid: int

@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
    print(f"Fetching age for user {wrapper.context.name}...")
    return f"User {wrapper.context.name} is 47 years old"

async def main():
    user_info = UserInfo(name="John", uid=123)

    agent = Agent[UserInfo](  
        name="Assistant",
        tools=[fetch_user_age],
        model=model,
        instructions="Always use <function_call>fetch_user_age</function_call> to fatch user age.",
    )

    result = await Runner.run(  
        starting_agent=agent,
        input="tell me about the user age",
        context=user_info,
    )

    print(result.final_output)  
    # The user John is 47 years old.

if __name__ == "__main__":
    asyncio.run(main())