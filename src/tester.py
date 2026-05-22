"""Testing module for the AI Python C Extensions Generator application."""

import io
import sys
from logging import getLogger


_logger = getLogger(__name__)


# Define a function to write outputs to a file with a given filename.
def write_file(data, filename):
    """Write data to a file with the specified filename."""
    with open(filename, "w") as file:
        file.write(data)


# Define a function to execute Python code and capture its output.
def execute_python(code):
    """Execute the given Python code and capture its output."""
    try:
        _logger.info('EXECUTING TEST CODE...')
        # Redirect stdout to capture the output of the executed code.
        output = io.StringIO()
        sys.stdout = output
        # Execute the provided code in a clean global namespace.
        exec(code, {})
    finally:
        # Restore original stdout.
        sys.stdout = sys.__stdout__
    return output.getvalue()


# Extension testing function.
def test_extension(usage_code):
    """Test the C extension executing the code and capture its output."""
    try:  # Write the code to file.
        write_file(usage_code, "usage_example.py")
    except Exception as ex:
        return f"An error occurred while writing test file:\n{ex}"
    try:
        # Execute the code and capture the output.
        output = execute_python(usage_code)
    except Exception as ex:
        return f"An error occurred while testing the extension:\n{ex}"
    return output
