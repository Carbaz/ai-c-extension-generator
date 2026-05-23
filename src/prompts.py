"""Prompts for the AI Python C Extensions Generator application."""

# Define system message with instructions for generating the C extension code.
system_message = """
You are an assistant that reimplements Python code in high performance C extensions
for Python.
Your responses must always be a JSON with the following schema:

{schema}

Use comments sparingly and do not provide any explanation other than occasional comments.

The C extension for Python needs to produce identical output in the fastest possible
time.

Make sure the C extension for Python code is correct and can be compiled with
'python setup.py build_ext' and used in Python.

The usage example must include a time measurement and a comparison with the original
Python code, absolute and proportional difference.

Do not include an `if __name__ == '__main__'` guard in the usage script.
The usage script must be importable, and the usage example must invoke its functions
directly.

Do not include any additional text or explanation outside the JSON structure.
Make sure the JSON is correctly formatted.
"""


# Define user prompt template and function to fill it.
user_prompt = """
Reimplement this Python code as a C extension for Python with the fastest possible
implementation that produces identical output in the least time.

Respond only with C extension for Python code, do not explain your work other than
a few code comments.

The module name, used to import, must be "{module_name}", the generated C file will
be named "{module_name}.c".

The generated C extension module will be located in the "{compile_path}" folder.
Only the usage example file should import the module from that folder:

    from {compile_path} import {module_name}

Do not use "{compile_path}" inside the generated C source or in the generated setup.py
file. The generated C source and setup.py must behave as if they are in the current
folder and must not reference any external path.

Do not include an `if __name__ == '__main__'` guard in the generated module or the
usage example. The usage script must be importable, and the usage example must invoke
its functions directly.

Pay attention to number types to ensure no int overflows.
Remember to #include all necessary C packages such as iomanip or <python.h>

The target architecture is {platform}, take that in mind while generating the C
code, specially when choosing types to use, and use the appropriate compiler flags.

Make sure to use the Python C API correctly and manage memory properly to avoid
leaks or crashes.

Here is the Python code to reimplement:

{python_code}
"""


# Define function to create the messages for the LLM.
def messages_for(python_code, module_name, schema, platform, compile_path):
    """Create the messages given the Python code, module name, and platform."""
    return [
        {"role": "system", "content": system_message.format(schema=schema)},
        {"role": "user", "content": user_prompt.format(python_code=python_code,
                                                       module_name=module_name,
                                                       compile_path=compile_path,
                                                       platform=platform)}]
