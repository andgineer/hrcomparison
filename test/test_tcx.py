from hrcomparison.tcx import TCXParser


def test_tcx():
    tcx = TCXParser('test/20180415_ski_garmin.tcx')
    assert tcx.hr_max == 160
    assert tcx.distance == 17524.94921875
    assert tcx.duration == 6238.0
