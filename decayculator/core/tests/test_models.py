from unittest.mock import patch

import pytest

from decayculator.core.entropy import GrowingNoiseEntropy
from decayculator.core.models import DecayingNumber


def test_decaying_number_returns_original_value_at_t0():
    entropy = GrowingNoiseEntropy(growth_rate=1.0)
    with patch("decayculator.core.models.time") as mock_time:
        mock_time.time.return_value = 1000.0
        dn = DecayingNumber(123.45, entropy_strategy=entropy)

        # Now simulate reading at the same time
        mock_time.time.return_value = 1000.0
        value = dn.read()
        assert value == pytest.approx(123.45, abs=1e-6)


def test_decaying_number_accumulates_noise():
    entropy = GrowingNoiseEntropy(growth_rate=1.0)
    with patch("decayculator.core.models.time") as mock_time:
        mock_time.time.return_value = 100.0
        dn = DecayingNumber(10.0, entropy_strategy=entropy)

        mock_time.time.return_value = 105.0
        value_5s = dn.read()

        mock_time.time.return_value = 120.0
        value_20s = dn.read()

        # These values will be noisy, just confirm they're floats and not constant
        assert isinstance(value_5s, float)
        assert isinstance(value_20s, float)
        assert value_5s != value_20s
