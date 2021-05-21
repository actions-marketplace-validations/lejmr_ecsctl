#!/usr/bin/env python

import argparse
from ecs import render, helper
import json
import logging


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Render ECS Task definition from template and input variables')
    parser.add_argument(
        '--td', help="Path to task definition (json, yaml, or even a directory)", default="task-definition.json")
    parser.add_argument(
        '--val', nargs="*", help="Path values used for interpolation of task definition (json, yaml, or even a directory)")
    parser.add_argument('--set', nargs="*",
                        help="Values overrides, e.g., name=NAME,value=VALUE")
    args = parser.parse_args()

    # Load variables from given files
    values, mvalues, ivalues = [], [], {}
    if not args.val is None:
        for v in args.val:
            values += render.load_path(v)
        mvalues = render.merge_dicts(values)

    # Override by variables loaded from argparse (TODO find a proper format)
    if not args.set is None:
        overrides = {}
        for s in args.set:
            try:
                a = helper.parse_value_override(s)
            except ValueError:
                logging.warning("Skiping argument {}".format(s))
                continue
            overrides = render.merge_dicts([overrides, a])
        mvalues = render.merge_dicts([mvalues, overrides])

    # Interpolate variables
    if len(mvalues):
        ivalues = render.interpolate_values(mvalues)

    # Load task definition
    td = render.load_path(args.td, ivalues)
    mtd = render.merge_dicts(td)

    # Generate output json file (ideally in pretty format)
    print(json.dumps(mtd, indent=4, sort_keys=True))
