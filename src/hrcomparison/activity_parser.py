from hrcomparison.base import ActivityParser
from hrcomparison.fit import FITParser
from hrcomparison.gpx import GPXParser
from hrcomparison.tcx import TCXParser


def get_parser(filename: str) -> ActivityParser:
    """Factory function to return appropriate parser based on file extension"""
    ext = filename.lower().split(".")[-1]
    if ext == "tcx":
        return TCXParser(filename)
    if ext == "gpx":
        return GPXParser(filename)
    if ext == "fit":
        return FITParser(filename)
    raise ValueError(f"Unsupported file format: {ext}")
