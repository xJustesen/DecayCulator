import time

from decayculator.core.entropy import AccumulatedNoiseEntropy, GrowingNoiseEntropy


def test_zero_noise_at_zero_age():
    entropy = GrowingNoiseEntropy(growth_rate=1.0)
    value = 42.0
    noisy_value = entropy.decay(value, age=0.0)
    assert noisy_value == value


def test_noise_increases_with_time():
    entropy = GrowingNoiseEntropy(growth_rate=0.5)
    value = 100.0

    # Since it's random, we check that standard deviation increases
    # over many samples (not deterministic, but reasonable)
    samples = [entropy.decay(value, age=10.0) for _ in range(1000)]
    std_dev = (sum((x - value) ** 2 for x in samples) / len(samples)) ** 0.5

    assert std_dev > 1.0


def test_noise_accumulates_over_time(mocker):
    entropy = AccumulatedNoiseEntropy(magnitude=1, step_freq=10)
    base_value = 100.0

    mock_time = mocker.patch("time.time")
    mock_time.return_value = 1000.0
    val1 = entropy.decay(base_value, age=0)

    mock_time.return_value = 1001.0  # simulate 1 second later
    val2 = entropy.decay(base_value, age=1.0)

    assert abs(val2 - val1) > 0.1, "Noise did not accumulate over time"


def test_independent_instances_do_not_share_state(mocker):
    entropy = AccumulatedNoiseEntropy(magnitude=0.1, step_freq=10)

    mock_time = mocker.patch("time.time")
    mock_time.return_value = 1000.0

    val1 = entropy.decay(100.0, 0)
    val2 = entropy.decay(200.0, 0)

    mock_time.return_value = 1001
    val1_later = entropy.decay(100.0, 1.0)
    val2_later = entropy.decay(200.0, 1.0)

    diff1 = val1_later - val1
    diff2 = val2_later - val2

    assert abs(diff1) > 0.01 and abs(diff2) > 0.01, "Noise did not accumulate independently"
    assert abs(diff1 - diff2) > 1e-6, "Noise state appears to be shared"
