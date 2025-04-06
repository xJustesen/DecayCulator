import random
import string

from textual.containers import Grid
from textual.message import Message
from textual.timer import Timer
from textual.widget import Widget
from textual.widgets import Button

from decayculator.core.entropy import GrowingNoiseEntropy
from decayculator.core.models import DecayingNumber


def _get_button_id(label: str) -> str:
    """Generate a unique button ID based on the label."""
    suffix = {"/": "divide", "*": "multiply", "-": "subtract", "+": "add", "=": "equals", ".": "decimal"}
    return f"btn-{suffix.get(label, label)}"


class DecayingButton(Button):
    def __init__(self, true_value: str, **kwargs):
        super().__init__(true_value, **kwargs)
        self.true_value = true_value
        self.corruption_timer: Timer | None = None

        # Only apply decay logic to numeric buttons
        if true_value.isdigit():
            float_val = float(true_value)
            self.decay_model = DecayingNumber(
                float_val, entropy_strategy=GrowingNoiseEntropy(growth_rate=0.1)
            )
        else:
            self.decay_model = None

    def on_mount(self):
        self.corruption_timer = self.set_interval(2.0, self.corrupt_label)

    def corrupt_label(self):
        if self.decay_model:
            value = self.decay_model.read()
            display = f"{value:.2f}"  # maybe show 2 decimal places for chaos
            if random.random() < 0.1:
                display = display.replace(".", random.choice([" ", "#", "▒"]))
            self.label = display
        else:
            # For non-digit buttons, fall back to traditional visual decay
            if random.random() < 0.1:
                self.label = random.choice(["@", "?", "!", " ", self.true_value])
            else:
                self.label = self.true_value

    def press(self) -> None:
        # Override press so original value is preserved
        self.label = self.true_value  # optional: flash true label
        self.set_timer(0.3, self.corrupt_label)  # re-corrupt shortly after
        super().press()


class ButtonGrid(Grid):
    class ButtonPressed(Message):
        def __init__(self, sender: Widget, label: str):
            super().__init__()
            self.label = label

    def __init__(self):
        super().__init__()

    def compose(self):
        # Layout in calculator-style grid
        buttons = [
            "7",
            "8",
            "9",
            "/",
            "4",
            "5",
            "6",
            "*",
            "1",
            "2",
            "3",
            "-",
            "0",
            ".",
            "=",
            "+",
            "C",
        ]
        for label in buttons:
            yield DecayingButton(label, id=_get_button_id(label), variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        label = getattr(event.button, "true_value", str(event.button.label))
        self.post_message(self.ButtonPressed(self, label))
