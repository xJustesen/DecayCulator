import time
from dataclasses import dataclass, field

from decayculator.core.entropy import EntropyStrategy
from decayculator.utils.logging import logger


@dataclass
class DecayingNumber:
    """A float-like object that decays over time."""

    original_value: float
    entropy_strategy: EntropyStrategy
    birth_time: float = field(default_factory=lambda: time.time())

    def read(self) -> float:
        """Returns the current, entropy-decayed value."""
        current_time = time.time()
        age = current_time - self.birth_time
        decayed = self.entropy_strategy.decay(self.original_value, age)

        logger.debug(
            f"DecayingNumber.read(): age={age:.2f}s, original={self.original_value}, decayed={decayed}"
        )

        return decayed

    def __repr__(self) -> str:
        return f"<DecayingNumber value={self.read():.5f}>"

    def __post_init__(self):
        logger.debug(
            f"DecayingNumber created: original={self.original_value}, entropy={type(self.entropy_strategy).__name__}"
        )
