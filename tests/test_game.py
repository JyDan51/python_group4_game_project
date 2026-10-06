"""
A + D
Testatkaa game.py:n pelilogiikkaa tässä.

Esimerkkejä:
- saman pisteen etäisyys = 0 km
- energia lasketaan oikein
- peli ei salli lentoa, jos energia ei riitä
- voittoehto toimii
"""

from game import calculate_distance


def test_same_location_distance():
    assert calculate_distance(60.0, 25.0, 60.0, 25.0) == 0
