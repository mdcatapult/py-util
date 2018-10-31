# -*- coding: utf-8 -*-
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="enable debug", action="store_true" )
parser.add_argument("--info", help="enable debug", action="store_true" )
args, unknown = parser.parse_known_args()

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

level = logging.ERROR

if args.info:
    level = logging.INFO
elif args.debug:
    level = logging.DEBUG

logging.basicConfig(level=level, format=LOG_FORMAT)

