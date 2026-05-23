"""Main entrypoint module for the AI Python C Extensions Generator application."""

from logging import getLogger
from os import getenv, sep
from pathlib import Path
from sys import platform

from .compiler import compile_extension
from .interface import get_interface
from .optimizer import optimize_gpt as optimize_function
from .tester import test_extension


_logger = getLogger(__name__)

# Default models list
DEFAULT_MODELS = ["gpt-5.1-codex", "gpt-5.4"]  # Expensive.
DEFAULT_MODELS = ["gpt-5.1-codex-mini", "gpt-5.4-mini"]  # Cheap.

# Read available models from environment variable or use defaults
models = models_env.split(":") if (models_env := getenv("MODELS")) else DEFAULT_MODELS

# Detect system platform for default selection.
if platform == "win32":
    default_platform = "Windows"
else:
    default_platform = "Linux"

# Read compile stage flag from environment variable, defaulting to False if not set.
if compile_stage := getenv("COMPILE_STAGE", "False").lower() in ("true", "1", "yes"):
    # Define the build directory for compiled extensions.
    BUILD_DIR = Path("compiled")
    # BUILD_DIR.mkdir(parents=True, exist_ok=True)
    _logger.info('COMPILE STAGE ENABLED')
    _logger.info(f'COMPILE DIRECTORY SET TO: .{sep}{BUILD_DIR}')


def main():
    """Launch the AI Python C Extensions Generator application."""
    _logger.info('STARTING AI PYTHON C EXTENSIONS GENERATOR...')
    _logger.info(f'AVAILABLE MODELS: {models}')
    # Prepare the interface configuration based.
    interface_config = {"models": models, "compile_stage": compile_stage,
                        "optimize_function": optimize_function}
    if compile_stage:
        interface_config.update({"compile_extension": compile_extension,
                                 "test_extension": test_extension,
                                 "compile_path": BUILD_DIR})
    app = get_interface(**interface_config)
    app.launch(footer_links=[])
    # We return the app instance for potential use in autoreload scenarios.
    return app


if __name__ == '__main__':
    main()
