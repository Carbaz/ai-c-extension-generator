"""Interface module for the AI Python C Extensions Generator application."""

from gradio import Blocks, Button, Dropdown, Examples, Markdown, Row, State, TextArea
from gradio import Textbox

from .examples import example_dict
from .prompts import footer_disclaimer


def _compile_extension():
    return "COMPILE_EXTENSION PLACEHOLDER"


def _test_extension():
    return "TEST_EXTENSION PLACEHOLDER"


def get_interface(optimize_function, compile_stage=False,
                  compile_extension=_compile_extension,
                  test_extension=_test_extension,
                  default_platform="Windows",
                  compile_path="compiled",
                  models=["gpt-5.1-codex-mini"]):
    """Get the Gradio Blocks interface for the AI Python C Extensions Generator."""
    with Blocks(title="AI Python C Extensions Generator") as ui:
        compile_path_st = State(value=compile_path)
        Markdown("## Convert code from Python to C Extension")

        with Row():
            module_name = Textbox(label="Module name:", lines=1, value="sample_module")
            model = Dropdown(label="Select model", choices=models, value=models[0])
            platform = Dropdown(label="Select platform", choices=["Windows", "Linux"],
                                value=default_platform)

        with Row():
            python = Textbox(label="Python code:", lines=30,
                             buttons=["copy"], elem_classes=["python"],
                             value=example_dict["Hello world"][0])
            c_code = Textbox(label="C Extension code:", lines=30,
                             buttons=["copy"], elem_classes=["c_ext"])

        with Row():
            Examples(label="Python examples: (From simple to complex)",
                     inputs=[python, module_name],
                     examples=list(example_dict.values()),
                     example_labels=list(example_dict.keys()))

        with Row():
            get_extension = Button("Generate extension code")

        with Row():
            setup_code = Textbox(label="Compilation code:", lines=10,
                                 buttons=["copy"], elem_classes=["python"])
            usage_code = Textbox(label="Test compare code:", lines=10,
                                 buttons=["copy"], elem_classes=["python"])

        get_extension.click(optimize_function,
                            inputs=[python, module_name, platform,
                                    compile_path_st, model],
                            outputs=[c_code, setup_code, usage_code])

        # ######### BUILD AND TEST SECTIONS ######### #
        if compile_stage:
            with Row():
                compile_ext = Button("Compile extension")
            with Row():
                c_ext_out = TextArea(label="C Extension result:", buttons=["copy"],
                                     elem_classes=["c_ext"])

            with Row():
                test_run = Button("Test code")
            with Row():
                test_out = TextArea(label="Test result:", buttons=["copy"],
                                    elem_classes=["python"])

            compile_ext.click(compile_extension,
                              inputs=[c_code, setup_code, module_name, compile_path_st],
                              outputs=[c_ext_out])

            test_run.click(test_extension,
                           inputs=[usage_code, compile_path_st],
                           outputs=[test_out])

    # Footer with disclaimer.
    with ui:
        Markdown(footer_disclaimer, elem_id="footer-disclaimer")

    return ui
