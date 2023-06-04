from tcx import TCXParser
from datetime import datetime


def test_tcx(tcx_file):
    tcx = TCXParser(tcx_file)
    assert tcx.hr_max == 160
    assert tcx.distance == 17524.94921875
    assert tcx.duration == 6238.0

    assert tcx.hr_avg == 137.33280632411066
    assert tcx.latitude == 60.17921760678291
    assert tcx.longitude == 30.538074485957623
    assert tcx.pace_avg == '05:55'
    assert tcx.hr_min == 59
    assert tcx.calories == 797
    assert tcx.distance_units == 'meters'
    assert isinstance(tcx.pace, list)
    assert tcx.completed_at == '2018-04-15T07:45:02.000Z'
    assert tcx.activity_type == 'other'
