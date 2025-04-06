# ui/display_panel.py

import random

from rich.text import Text
from textual.reactive import reactive
from textual.timer import Timer
from textual.widget import Widget

from decayculator.core.calculator import Calculator
from decayculator.core.models import DecayingNumber


def _corrupt_expression(expr: str, corruption_chance: float = 0.1) -> str:
    corrupted = []
    noise_chars = ["@", "#", "?", "▒", "¶", "!", " "]
    for char in expr:
        if random.random() < corruption_chance:
            corrupted.append(random.choice(noise_chars))
        else:
            corrupted.append(char)
    return "".join(corrupted)


class DisplayPanel(Widget):
    expression: reactive[str] = reactive("")
    result: DecayingNumber | None = None
    refresh_timer: Timer | None = None

    def __init__(self, calculator: Calculator):
        super().__init__()
        self.calculator = calculator

    def set_expression(self, expr: str, evaluate: bool = False):
        self.expression = expr
        self.displayed_input = expr
        try:
            if evaluate:
                self.result = self.calculator.evaluate(expr)

            if self.refresh_timer:
                self.refresh_timer.stop()

            self.refresh_timer = self.set_interval(0.5, self.refresh_display)
            self.refresh()
        except Exception:
            self.result = None
            self.displayed_input = expr
            self.refresh()

    def refresh_display(self):
        # update corrupted input and refresh result
        self.displayed_input = _corrupt_expression(self.expression, corruption_chance=0.1)
        self.refresh()

    def render(self) -> Text:
        value = self.result.read() if self.result else "---"
        return Text.assemble(
            ("Input: ", "bold white"),
            (self.displayed_input + "\n", "bold magenta"),
            ("Output: ", "bold white"),
            (f"{value:.6f}" if isinstance(value, float) else str(value), "bold green"),
        )
