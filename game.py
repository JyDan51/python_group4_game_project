"""
SKY-SCAVENGER 2488
D:n tiedosto — Gameplay & Math Developer

SINUN VASTUUSI:
1. Laske kahden lentokentän välinen etäisyys Haversine-kaavalla.
2. Laske lennon energiankulutus etäisyyden perusteella.
3. Tarkista, riittääkö pelaajan energia lentoon.
4. Vähennä lennon jälkeen käytetty energia.
5. Laske rahtisopimuksesta saatava palkkio.
6. Lisää onnistuneen toimituksen palkkio pelaajan rahaan.
7. Tee energian ostamiseen tarvittava pelilogiikka.
8. Tarkista voittoehto (tavoiterahamäärä saavutettu).
9. Tarkista häviöehdot.

TÄMÄ TIEDOSTO EI HOIDA:
- SQL-kyselyitä
- päävalikkoa
- käyttäjän tekstisyötteiden tarkistamista
"""

from math import radians, sin, cos, sqrt, atan2


def calculate_distance(lat1, lon1, lat2, lon2):
    """Laskee kahden pisteen välisen etäisyyden kilometreinä."""
    earth_radius = 6371.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius * c


def calculate_energy(distance):
    """Laskee lennon energiankulutuksen."""
    # TODO D: päättäkää ryhmän kanssa sopiva energiakaava.
    pass


def can_fly(current_energy, required_energy):
    """Tarkistaa, riittääkö energia lentoon."""
    # TODO D
    pass


def calculate_reward(distance):
    """Laskee rahtisopimuksen palkkion."""
    # TODO D
    pass


def check_win(money, target_money):
    """Tarkistaa, onko pelaaja saavuttanut tavoiterahamäärän."""
    # TODO D
    pass
