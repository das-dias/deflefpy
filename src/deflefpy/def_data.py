"""_summary_
A Python implementation for the DEF data structures.
"""
# TODO
from loguru import logger
from util import Unsupported
import os


def test():
    feat = Unsupported("DEF Data Structures")
    logger.info(f"{str(feat)}")
    logger.info(f"Project File: {os.path.abspath(__file__)}")
