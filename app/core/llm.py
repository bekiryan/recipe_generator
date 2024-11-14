import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def chat_completion(message, model="gpt-4o"):
    """A helper function to interact with OpenAI's chat completion API.

    :param message: str: The message to send to the model.
    :param model: str: The model to use for the completion.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.choices[0].message.content.strip()
