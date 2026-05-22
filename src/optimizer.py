"""Optimizer module for the AI Python C Extensions Generator application."""

from logging import getLogger

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from .prompts import messages_for


_logger = getLogger(__name__)


# Environment initialization.
load_dotenv(override=True)


# Initialize client and set the default LLM model to use.
openai = OpenAI()
OPENAI_MODEL = "gpt-5"
_logger.info(f'INITIALIZED OPTIMIZER MODULE')


# Define Pydantic model class for GPT response parsing.
class _extension_codes(BaseModel):
    c_code: str
    setup: str
    usage: str

    def __str__(self):
        """Return a string representation of the optimization codes."""
        return (f"C CODE:\n{self.c_code}\n"
                f"---------------------------\n"
                f"setup.py:\n{self.setup}\n"
                f"---------------------------\n"
                f"USAGE:\n{self.usage}")


# Define optimization function using OpenAI's GPT model.
def optimize_gpt(python_code, module_name, platform, model=OPENAI_MODEL):
    """Generate an optimized C extension for Python."""
    schema = _extension_codes.model_json_schema()
    response = openai.chat.completions.parse(
        model=model, messages=messages_for(python_code, module_name, schema, platform),
        response_format=_extension_codes).choices[0].message.parsed
    return response.c_code, response.setup, response.usage
