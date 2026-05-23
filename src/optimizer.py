"""Optimizer module for the AI Python C Extensions Generator application."""

from logging import getLogger

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

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
    c_code: str = Field(...,
                        description="Generated C extension source "
                                    "code for the Python module.")
    setup: str = Field(...,
                       description="The generated setup.py build script "
                                   "used to compile the C extension module."
                                   "It must assume the module is in the current folder "
                                   "and not in any subfolder.")
    usage: str = Field(...,
                       description="A Python usage example that imports the compiled "
                                   "extension and compares its execution time with the "
                                   "original Python implementation.")

    def __str__(self):
        """Return a string representation of the optimization codes."""
        return (f"C CODE:\n{self.c_code}\n"
                f"---------------------------\n"
                f"setup.py:\n{self.setup}\n"
                f"---------------------------\n"
                f"USAGE:\n{self.usage}")


# Define optimization function using OpenAI's GPT model.
def optimize_gpt(python_code, module_name, platform, compile_path, model=OPENAI_MODEL):
    """Generate an optimized C extension for Python."""
    schema = _extension_codes.model_json_schema()
    _logger.info('SENDING OPTIMIZATION REQUEST TO OPENAI... '
                 f'(MODEL: {model}, PLATFORM: {platform}, '
                 f'MODULE: {module_name}, COMPILE PATH: {compile_path})')
    response = openai.responses.parse(
        model=model, text_format=_extension_codes,
        input=messages_for(python_code, module_name, schema, platform, compile_path)
        ).output_parsed
    _logger.info('RECEIVED OPTIMIZATION RESPONSE FROM OPENAI')
    return response.c_code, response.setup, response.usage
