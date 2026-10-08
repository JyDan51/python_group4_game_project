
from game import calculate_distance


def test_same_location_distance():
    assert calculate_distance(60.0, 25.0, 60.0, 25.0) == 0
