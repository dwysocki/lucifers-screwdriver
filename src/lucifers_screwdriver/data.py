import numpy as _np
from . import enums

__mpcorp_header_length = 41

__mpcorp_column_widths = [
    7, 1, 5, 24, 9, 2, 9, 2, 9, 2, 9, 13, 11, 2, 1, 11, 5, 1, 3
]

__mpcorp_usecols = [
    0, 2, 4, 6, 8, 10, 12, 14, 16, 18
]

__mpcorp_names = [
    enums.NAME, "",
    enums.H, "",
    enums.ARG_PERI, "",
    enums.LONG_ASC_NODE, "",
    enums.I, "",
    enums.E, "",
    enums.A, "",
    enums.UNCERT_FLAG, "",
    enums.N_OBS, "",
    enums.N_OPP
]

def read_mpcorp(filename,
                skip_header=__mpcorp_header_length,
                **kwargs):
    return _np.genfromtxt(filename,
                          delimiter=__mpcorp_column_widths,
                          usecols=__mpcorp_usecols,
                          names=__mpcorp_names,
                          skip_header=skip_header,
                          dtype=None,
                          **kwargs)
