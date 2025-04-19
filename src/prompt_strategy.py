from enum import Enum


class PromptStrategy(str, Enum):
    """
    An enumeration for specifying different prompt strategies used in
    generating text completions. Each strategy corresponds to a specific
    approach in providing examples to the model.

    Attributes:
        ZERO_SHOT (str): Strategy with no examples provided.
        ONE_SHOT (str): Strategy with one example provided.
        FEW_SHOT (str): Strategy with multiple examples provided.
    """

    ZERO_SHOT = 'ZERO_SHOT'
    ONE_SHOT = 'ONE_SHOT'
    FEW_SHOT = 'FEW_SHOT'

    def __str__(self):
        return self.value

    @staticmethod
    def from_string(s):
        try:
            return PromptStrategy[s]
        except KeyError:
            raise ValueError("Unknown key for prompt strategy")
