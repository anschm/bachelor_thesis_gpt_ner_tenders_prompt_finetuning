import time

from openai import OpenAI

from prompt_response import PromptResponse


class OpenAiClient:
    """
    A client for interacting with the OpenAI API to generate text completions.

    Attributes:
        model (str): The language model to use for generating completions.
        role (str): The role or identity context for the interactions.
        client (OpenAI): An instance of the OpenAI API client initialized with the given API key.
    """

    def __init__(self, model: str, role: str, api_key: str):
        """
        Initializes an OpenAI client with the specified model, role, and API key.

        Args:
            model (str): The language model to use for generating completions.
            role (str): The role or identity context for the interactions.
            api_key (str): The API key for authenticating with the OpenAI API.
        """
        self.model = model
        self.role = role
        self.client = OpenAI(api_key=api_key)

    def complete(self, prompt: str) -> PromptResponse:
        """
        Sends a completion request to the OpenAI API using the provided prompt.
        
        Args:
            prompt (str): The input text prompt for which the API should generate a completion.

        Returns:
            PromptResponse: An object containing the completion result and metadata,
                            including duration, total tokens, completion tokens, and prompt tokens.
        """
        start_time = time.time()

        completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": self.role,
                    "content": prompt,
                }
            ],
            model=self.model,
        )
        end_time = time.time()
        duration = end_time - start_time
        total_tokens = completion.usage.total_tokens
        completion_tokens = completion.usage.completion_tokens
        prompt_tokens = completion.usage.prompt_tokens

        response = PromptResponse()
        choices = completion.choices
        if choices is not None:
            response.html_result = choices[0].message.content
        else:
            response.html_result = None

        response.duration = duration
        response.total_tokens = total_tokens
        response.completion_tokens = completion_tokens
        response.prompt_tokens = prompt_tokens
        return response
