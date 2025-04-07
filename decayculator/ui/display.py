import random

from rich.text import Text
from textual.reactive import reactive
from textual.timer import Timer
from textual.widget import Widget

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
    displayed_input: reactive[str] = reactive("")
    result: DecayingNumber | None = None
    refresh_timer: Timer | None = None

    def set_expression(self, expr: str):
        self.expression = expr
        self.displayed_input = expr
        self.refresh()

    def set_result(self, result: DecayingNumber | None):
        self.result = result

        if self.refresh_timer:
            self.refresh_timer.stop()

        self.refresh_timer = self.set_interval(0.5, self.refresh_display)
        self.refresh()

    def refresh_display(self):
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
