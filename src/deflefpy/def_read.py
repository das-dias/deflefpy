"""_summary_
A Python implementation for the DEF file reader.
Supports .def, .json, and .yaml file output.
"""
# TODO
from loguru import logger
from deflefpy.util import Unsupported
import os


def test():
    feat = Unsupported("DEF Read")
    logger.info(f"{str(feat)}")
    logger.info(f"Project File: {os.path.abspath(__file__)}")
