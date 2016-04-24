"""
Functions for determining threats.
"""

def PHA(MOID, H, MOID_threshold, H_threshold):
    return (MOID < MOID_threshold) & (H < H_threshold)
