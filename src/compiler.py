"""Compilation and tests module for the AI Python C Extensions Generator application."""

import os
import subprocess
import sys
from logging import getLogger


_logger = getLogger(__name__)


# Define a function to write outputs to a file with a given filename.
def write_file(data, path):
    """Write data to a file with the specified filename."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as file:
        file.write(data)


# Extension compilation function.
def build_extension(compile_path):
    """Compile the C extension using 'setup.py' and return the compilation output."""
    # Set default COMSPEC to cmd.exe on Windows to avoid issues with some C compilers.
    if sys.platform == "win32":
        _logger.info('PATCHING COMSPEC FOR WINDOWS COMPILATION COMPATIBILITY...')
        preset_comspec = os.environ.get("COMSPEC")
        os.environ["COMSPEC"] = "C:\\Windows\\System32\\cmd.exe"
    try:
        _logger.info('STARTING COMPILATION PROCESS...')
        compile_cmd = ["python", "setup.py", "build_ext", "--inplace"]
        compile_result = subprocess.run(compile_cmd, env=os.environ, cwd=compile_path,
                                        check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as ex:
        _logger.error(f"COMPILATION FAILED WITH ERROR:\n{ex.stdout}\n{ex.stderr}")
        raise Exception(f"An error occurred while building:\n{ex.stdout}\n{ex.stderr}")
    finally:
        # Restore original COMSPEC on Windows.
        if sys.platform == "win32":
            _logger.info('RESTORING ORIGINAL COMSPEC...')
            os.environ["COMSPEC"] = preset_comspec
    _logger.info('COMPILATION COMPLETED SUCCESSFULLY.')
    return compile_result.stdout


# Extension compilation function.
def compile_extension(c_code, setup_code, module_name, compile_path):
    """Build the C extension from the provided codes."""
    try:  # Write the provided codes to their respective files.
        _logger.info('WRITING GENERATED C CODE TO FILE...')
        write_file(c_code, compile_path / f"{module_name}.c")
        _logger.info('WRITING GENERATED SETUP CODE TO FILE...')
        write_file(setup_code, compile_path / "setup.py")
    except Exception as ex:
        _logger.error(f"ERROR WHILE WRITING FILES:\n{ex}")
        return f"An error occurred while writing files:\n{ex}"
    try:  # Build the extension and capture the output.
        _logger.info('BUILDING THE EXTENSION...')
        build_output = build_extension(compile_path)
    except Exception as ex:  # If build fails, return the error message.
        _logger.error(f"ERROR WHILE BUILDING EXTENSION:\n{ex}")
        return str(ex)
    _logger.info('EXTENSION BUILT SUCCESSFULLY.')
    return build_output
