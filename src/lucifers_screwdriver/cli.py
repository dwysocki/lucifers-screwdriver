"""
Command line interface.
"""
from argparse import ArgumentParser
import tempfile as temp
import numpy as np
from .data import read_mpcorp
from . import enums as _e
from . import ml
from . import sim
from . import threat

def simulate(args, data, earth_data):
    MOID = None

    try:
        if args.working_dir is None:
            tmpdir = temp.TemporaryDirectory()
            args.working_dir = tmpdir.name
        else:
            tmpdir = None

        sim.simulate(args.MOID_exe, args.working_dir,
                     data, earth_data, args.MOID_output)

    finally:
        if tmpdir is not None:
            tmpdir.close()


def learn(args, data, earth_data):
    valid_idx = np.isfinite(data[_e.H])
    data = data[valid_idx]

    MOID = np.loadtxt(args.MOID_input)[valid_idx]
    PHA = threat.PHA(MOID, data[_e.H], args.MOID_threshold, args.H_threshold)

    clf = ml.train(data, PHA, n_neighbors=args.n_neighbors)

    predictions = clf.predict(ml.features(data))

    completeness, contamination = ml.performance(PHA, predictions)

    print("Completeness  = {:.3}%".format(completeness*100))
    print("Contamination = {:.3}%".format(contamination*100))



def get_args():
    p = ArgumentParser(
        prog="lucifers-screwdriver"
    )

    sub_p = p.add_subparsers()

    sim_p = sub_p.add_parser("sim", help="Run simulation.")
    learn_p = sub_p.add_parser("learn", help="Train model.")

    sim_p.set_defaults(func=simulate)
    learn_p.set_defaults(func=learn)

    p.add_argument(
        "--orbit-data",
        help="MPCORB data file."
    )

    p.add_argument(
        "--MOID-threshold", default=0.05,
        help="MOID threshold to be classified as a PHA (default 0.05)."
    )
    p.add_argument(
        "--H-threshold", default=22.0,
        help="Magnitude threshold to be classified as a PHA (default 22.0)."
    )

    p.add_argument(
        "--earth-a", default=1.00000011,
        help="Semi-major axis of Earth's orbit (default 1.00000011 AU)")
    p.add_argument(
        "--earth-e", default=0.01671022,
        help="Eccentricity of Earth's orbit (default 0.01671022)."
    )
    p.add_argument(
        "--earth-i", default=0.00005,
        help="Inclination of Earth's orbit (default 0.00005 degrees)."
    )
    p.add_argument(
        "--earth-longitude-asc-node", default=-11.26064,
        help="Longitude of ascending node of Earth's orbit "
             "(default -11.26064 degrees)."
    )
    p.add_argument(
        "--earth-arg-periapsis", default=102.94719,
        help="Argument of periapsis of Earth's orbit "
             "(default 102.94719 degrees)."
    )


    sim_p.add_argument(
        "--MOID-exe", required=True,
        help="MOID simulation executable."
    )
    sim_p.add_argument(
        "--MOID-output", required=True,
        help="File to write MOIDs to."
    )
    sim_p.add_argument(
        "--working-dir", default=".",
        help="(Optional) working directory for simulations."
    )

    learn_p.add_argument(
        "--MOID-input", required=True,
        help="File to read MOIDs from."
    )
    learn_p.add_argument(
        "--n-neighbors", default=2, type=int,
        help="Number of neighbors to use (default 2)."
    )

    args = p.parse_args()

    return args


def main():
    args = get_args()

    orbit_data = read_mpcorp(args.orbit_data)
    earth_data = np.rec.array(
        (args.earth_a, args.earth_e, args.earth_i,
          args.earth_longitude_asc_node, args.earth_arg_periapsis),
        dtype=[(_e.A, float), (_e.E, float), (_e.I, float),
               (_e.LONG_ASC_NODE, float), (_e.ARG_PERI, float)]
    )

    args.func(args, orbit_data, earth_data)
