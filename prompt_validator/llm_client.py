# File: prompt_validator/llm_client.py
import os # Import os for environment variable access.
from openai import OpenAI # Import the OpenAI client.
from dotenv import load_dotenv # Import function to load .env files.

load_dotenv() # Load environment variables from a .env file.

class LLMClient: # A client to interact with the Language Model.
    def __init__(self): # Initialize the LLMClient.
        api_key = os.getenv("OPENAI_API_KEY") # Get API key from environment.
        if not api_key: # Check if the API key is set.
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.client = OpenAI(api_key=api_key) # Instantiate the OpenAI client.

    def query(self, system_prompt: str, user_prompt: str) -> str: # Query the LLM with given prompts.
        try: # Try to get a response from the chat completion endpoint.
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo", # Specify the model to use.
                messages=[
                    {"role": "system", "content": system_prompt}, # Set the system's role and instructions.
                    {"role": "user", "content": user_prompt}, # Provide the user's content.
                ],
                temperature=0.0, # Set temperature to 0 for deterministic output.
            )
            return response.choices[0].message.content.strip() # Return the content of the first choice.
        except Exception as e: # Catch any exceptions during the API call.
            return f"Error querying LLM: {e}" # Return an error message.