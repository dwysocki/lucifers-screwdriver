"""
MOID Simulations.
"""
import numpy as np
from . import enums as _e
from .kepler import periapsis
from .utils import cd
from os import path
import subprocess as sub


def input_line(params):
    sem_maj_axis  = params[_e.A]
    eccentricity  = params[_e.E]
    inclination   = params[_e.I]
    long_asc_node = params[_e.LONG_ASC_NODE]
    arg_peri      = params[_e.ARG_PERI]

    peri_dist = periapsis(sem_maj_axis, eccentricity)

    return " ".join([
        "{0:.10f}".format(float(x)) for x in
        [peri_dist, eccentricity, inclination, long_asc_node, arg_peri]
    ]) + "\n"


def make_input_file(directory, object_params, earth_params):
    filename = path.join(directory, "orbit_data.inp")

    with open(filename, "w") as f:
        f.write(input_line(earth_params))
        f.write(input_line(object_params))


def read_output_file(directory):
    filename = path.join(directory, "critpts.out")
    with open(filename, "r") as f:
        MOID = np.inf
        for line in f:
            v1, v2, dist, type = line.split()

            if type == "MINIMUM":
                MOID = np.min([MOID, float(dist)])

    return MOID


def run_sim(exe, directory):
    exe_path = path.abspath(exe)
    with cd(directory):
        sub.run(exe_path, stdout=sub.DEVNULL)


def simulate(exe, directory, object_params, earth_params):
    MOID = np.empty(len(object_params), dtype=float)

    for i in range(len(object_params)):
        make_input_file(directory, object_params[i], earth_params)
        run_sim(exe, directory)
        MOID[i] = read_output_file(directory)

    return MOID
