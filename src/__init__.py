"""Initialization module for the AI Python C Extensions Generator application."""

from logging import basicConfig, getLogger

from dotenv import load_dotenv


# Environment initialization.
load_dotenv(override=True)

# Setup the global logger.
LOG_STYLE = '{'
LOG_LEVEL = 'INFO'
LOG_FORMAT = ('{asctime} {levelname:<8} {processName}({process}) '
              '{threadName} {name} {lineno} "{message}"')
basicConfig(level=LOG_LEVEL, style='{', format=LOG_FORMAT)

getLogger(__name__).info('INITIALIZED AI PYTHON C EXTENSIONS GENERATOR')
