"""
Keplerian orbit calculations.
"""

def periapsis(semi_major_axis, eccentricity):
    return (1 - eccentricity) * semi_major_axis
