from src.tcx import TCXParser


def test_tcx(tcx_file):
    tcx = TCXParser(tcx_file)
    assert tcx.hr_max == 160
    assert tcx.distance == 17524.94921875
    assert tcx.duration == 6238.0
