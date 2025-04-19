class PromptResponse:
    """
    Represents the response from an OpenAI prompt completion, capturing
    the result and associated metadata.

    Attributes:
        html_result (str | None): The content of the response, possibly in HTML format.
                                  None if no content is available.
        total_tokens (int): The total number of tokens used in the prompt and completion.
        completion_tokens (int): The number of tokens in the completion itself.
        prompt_tokens (int): The number of tokens in the prompt sent to the API.
        duration (float): The time taken to receive the completion response in seconds.
    """
    html_result: str | None
    total_tokens: int
    completion_tokens: int
    prompt_tokens: int
    duration: float
