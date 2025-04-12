import asyncio

from agents import Agent, ItemHelpers, Runner, trace
from LLMConfig import model

"""
This example shows the parallelization pattern. We run the agent three times in parallel, and pick
the best result.
"""

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
    model=model,
)

french_agent = Agent(
    name="french_agent",
    instructions="You translate the user's message to French",
    model=model,
)

german_agent = Agent(
    name="german_agent",
    instructions="You translate the user's message to German",
    model=model,
)

translation_picker = Agent(
    name="translation_picker",
    instructions="You pick the best Spanish translation from the given options.",
    model=model,
)


async def main():
    print("Your message will be translated to Spanish, french, and german.")
    print("Then, the one with the best Spanish translation will be picked.\n")
    msg = input("Hi! Enter a message: ")

    # Ensure the entire workflow is a single trace
    with trace("Parallel translation"):
        res_1, res_2, res_3 = await asyncio.gather(
            Runner.run(
                spanish_agent,
                msg,
            ),
            Runner.run(
                french_agent,
                msg,
            ),
            Runner.run(
                german_agent,
                msg,
            ),
        )

        outputs = [
            ItemHelpers.text_message_outputs(res_1.new_items),
            ItemHelpers.text_message_outputs(res_2.new_items),
            ItemHelpers.text_message_outputs(res_3.new_items),
        ]

        translations = "\n\n".join(outputs)
        print(f"\n\nTranslations:\n\n{translations}")

        best_translation = await Runner.run(
            translation_picker,
            f"Input: {msg}\n\nTranslations:\n{translations}",
        )

    print("\n\n-----")

    print(f"Best Spanish Translation: {best_translation.final_output}")


if __name__ == "__main__":
    asyncio.run(main())