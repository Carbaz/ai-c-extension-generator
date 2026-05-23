"""Entrypoint wrapper for Hugging Face Spaces. Delegates to src/__main__.py."""

import argparse

from src.__main__ import main


# HBD: We assign the 'app' to 'demo' to allow watch autoreload:
# 'demo' is required to be defined at the global scope for reload to work in Gradio.
# Initial warnings may appear at launch with 'gradio app.py' because 'demo' will not
# exists until the app service ends inside main, but it will do when reload requires it,
# once the service has been stopped.

parser = argparse.ArgumentParser(description="AI Python C Extensions Generator")
parser.add_argument("-c", "--compile-stage", action="store_true", default=False,
                    help="Enable compile stage in the interface")
args = parser.parse_args()

demo = main(compile_stage=args.compile_stage)
