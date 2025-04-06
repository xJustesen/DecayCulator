import random
import time
from abc import ABC, abstractmethod

from decayculator.utils.logging import logger


class EntropyStrategy(ABC):
    @abstractmethod
    def decay(self, base_value: float, age: float) -> float: ...


class GrowingNoiseEntropy(EntropyStrategy):
    """
    Entropy strategy where noise increases with time, making values increasingly inaccurate over time.
    This strategy is stateless but will add an increasing amount of noise to the value based on its age.
    """

    def __init__(self, growth_rate: float = 0.1):
        """
        :param growth_rate: Noise grows as `growth_rate * age`
        """
        self.growth_rate = growth_rate

    def decay(self, value: float, age: float) -> float:
        """
        Add zero-centered noise whose standard deviation grows with time.
        """
        std_dev = self.growth_rate * age
        noise = random.gauss(0, std_dev)
        decayed = value + noise
        logger.debug(
            f"Entropy applied: value={value}, age={age:.2f}s, std_dev={std_dev:.3f}, noise={noise:.5f}, result={decayed:.5f}"
        )
        return decayed


class AccumulatedNoiseEntropy(EntropyStrategy):
    """
    Accumulates noise over time, making values increasingly inaccurate.
    This strategy is stateful and will add noise to the value based on the time since the last update.
    """

    def __init__(self, magnitude: float = 0.05, step_freq: float = 10.0):
        """
        :param std_dev_per_step: Noise magnitude per update tick
        :param step_freq: Number of noise steps per second
        """
        self.magnitude = magnitude
        self.step_freq = step_freq

        self._last_update_time: dict[int, float] = {}
        self._accumulated_noise: dict[int, float] = {}

    def decay(self, base_value: float, age: float) -> float:
        obj_id = id(base_value)  # treat each base_value as separate entropy track
        now = time.time()

        if obj_id not in self._last_update_time:
            self._last_update_time[obj_id] = now
            self._accumulated_noise[obj_id] = 0.0

        last_time = self._last_update_time[obj_id]
        steps = int((now - last_time) * self.step_freq)

        for _ in range(steps):
            noise = random.gauss(0, self.magnitude)
            self._accumulated_noise[obj_id] += noise

        self._last_update_time[obj_id] = now
        return base_value + self._accumulated_noise[obj_id]
