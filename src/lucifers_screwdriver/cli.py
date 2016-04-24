"""
Command line interface.
"""
from argparse import ArgumentParser
import tempfile as temp
import numpy as np
from .data import read_mpcorp
from . import enums as _e
from . import sim


def simulate(args, data, earth_data):
    MOID = None

    try:
        if args.working_dir is None:
            tmpdir = temp.TemporaryDirectory()
            args.working_dir = tmpdir.name
        else:
            tmpdir = None

        MOID = sim.simulate(args.MOID_exe, args.working_dir,
                            data, earth_data)

    finally:
        if tmpdir is not None:
            tmpdir.close()

    if MOID is not None:
        print(MOID)
    else:
        raise Exception()


def train(args, earth_data, data):
    pass

def predict(args, earth_data, data):
    pass


def get_args():
    p = ArgumentParser(
        prog="lucifers-screwdriver"
    )

    sub_p = p.add_subparsers()

    sim_p = sub_p.add_parser("sim", help="Run simulation.")
    train_p = sub_p.add_parser("train", help="Train model.")
    predict_p = sub_p.add_parser("predict", help="Make predictions.")

    sim_p.set_defaults(func=simulate)
    train_p.set_defaults(func=train)
    predict_p.set_defaults(func=predict)

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


    # Earth Parameters
#    p.add_argument(
#    )


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


    args = p.parse_args()

    return args



def main():
    args = get_args()

    orbit_data = read_mpcorp(args.orbit_data, skip_header=700000)
    earth_data = np.rec.array(
        (args.earth_a, args.earth_e, args.earth_i,
          args.earth_longitude_asc_node, args.earth_arg_periapsis),
        dtype=[(_e.A, float), (_e.E, float), (_e.I, float),
               (_e.LONG_ASC_NODE, float), (_e.ARG_PERI, float)]
    )

    args.func(args, orbit_data, earth_data)
