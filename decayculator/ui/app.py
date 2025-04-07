import argparse

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from decayculator.core.calculator import Calculator
from decayculator.core.entropy import AccumulatedNoiseEntropy
from decayculator.ui.buttons import ButtonGrid
from decayculator.ui.display import DisplayPanel
from decayculator.utils.logging import configure_logger, logger


class DecayCulatorApp(App):
    CSS_PATH = "calculator.tcss"

    def __init__(self):
        super().__init__()
        self.calculator = Calculator(entropy_strategy=AccumulatedNoiseEntropy())
        self.current_expression = ""

    def compose(self) -> ComposeResult:
        with Vertical(id="container"):
            yield Static("🧮 DecayCalculator", id="title")
            self.display_panel = DisplayPanel()
            yield self.display_panel
            yield ButtonGrid()

    def on_mount(self) -> None:
        self.display_panel.set_expression("")

    def on_button_grid_button_pressed(self, event: ButtonGrid.ButtonPressed):
        label = event.label
        # You’ll handle input building here next!
        logger.debug(f"Button pressed: {label}; current expression: {self.current_expression}")

        if label == "=":
            # Try to evaluate
            try:
                result = self.calculator.evaluate(self.current_expression)
                self.display_panel.set_expression(self.current_expression)
                self.display_panel.set_result(result)
                self.current_expression = ""
            except Exception:
                self.display_panel.set_expression("ERROR")
                self.display_panel.set_result(None)
        elif label == "C":
            # Clear the expression
            self.current_expression = ""
            self.display_panel.set_expression("")  # also resets corruption and result
            self.display_panel.result = None
        else:
            # Add to expression
            self.current_expression += label
            self.display_panel.set_expression(self.current_expression)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DecayCulator: An Entropic Calculator")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    configure_logger(debug_mode=args.debug)

    logger.info("Starting DecayCulator...")
    app = DecayCulatorApp()
    app.run()
    logger.info("DecayCulator has exited.")
