from hrcomparison.tcx import TCXParser


def test_tcx():
    tcx = TCXParser('tests/20180415_ski_garmin.tcx')
    assert tcx.hr_max == 160
