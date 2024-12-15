import pytest
from datetime import datetime
from tcx import TCXParser
from activity_parser import get_parser
from fit import FITParser
from gpx import GPXParser


def test_tcx(tcx_file):
    tcx = TCXParser(tcx_file)
    assert tcx.hr_max == 160
    assert tcx.distance == 17524.94921875
    assert tcx.duration == 6238.0

    assert tcx.hr_avg == 137.33280632411066
    assert tcx.latitude == 60.17921760678291
    assert tcx.longitude == 30.538074485957623
    assert tcx.pace_avg == "05:55"
    assert tcx.hr_min == 59
    assert tcx.calories == 797
    assert tcx.distance_units == "meters"
    assert isinstance(tcx.pace, list)
    assert tcx.completed_at == "2018-04-15T07:45:02.000Z"
    assert tcx.activity_type == "other"


def test_gpx_parser_basic(gpx_file):
    parser = GPXParser(gpx_file)
    assert len(parser.time_values) == 2
    assert len(parser.hr_values) == 2
    assert parser.hr_values == [140, 145]
    assert parser.hr_max == 145
    assert parser.hr_min == 140
    assert parser.hr_avg == 142.5
    assert parser.latitude == pytest.approx(60.17921760)
    assert parser.longitude == pytest.approx(30.53807448)
    assert parser.activity_type == "other"
    assert isinstance(parser.completed_at, datetime)
    assert parser.distance > 0  # Should be calculated from coordinates
    assert parser.duration == 10.0  # 10 seconds between points
    assert isinstance(parser.pace, list)
    assert parser.calories == 0  # GPX doesn't include calories
    assert parser.distance_units == "meters"
    assert isinstance(parser.pace_avg, str)


def test_fit_parser_basic(fit_file):
    parser = FITParser(fit_file)
    assert len(parser.time_values) == 3
    assert len(parser.hr_values) == 3
    assert parser.hr_values == [140, 141, 142]
    assert parser.hr_max == 142
    assert parser.hr_min == 140
    assert parser.hr_avg == 141
    assert parser.latitude == pytest.approx(60.17921760)
    assert parser.longitude == pytest.approx(30.53807448)
    assert parser.activity_type == "running"
    assert isinstance(parser.completed_at, datetime)
    assert parser.calories == 500
    assert parser.distance == 200  # Last distance value
    assert parser.duration == 2.0  # 2 seconds between first and last point
    assert isinstance(parser.pace, list)
    assert parser.distance_units == "meters"
    assert isinstance(parser.pace_avg, str)


def test_get_parser_tcx(tcx_file):
    parser = get_parser(tcx_file)
    assert isinstance(parser, TCXParser)


def test_get_parser_gpx(gpx_file):
    parser = get_parser(gpx_file)
    assert isinstance(parser, GPXParser)


def test_get_parser_fit(fit_file):
    parser = get_parser(fit_file)
    assert isinstance(parser, FITParser)


def test_get_parser_invalid():
    with pytest.raises(ValueError):
        get_parser("test.invalid")


def test_get_parser_invalid_additional():
    for ext in ["jpg", "txt", "pdf"]:
        with pytest.raises(ValueError):
            get_parser(f"test.{ext}")


def test_tcx_parser_no_heartrate(tmp_path):
    content = """<?xml version="1.0" encoding="UTF-8"?>
<TrainingCenterDatabase xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2">
    <Activities>
        <Activity Sport="Other">
            <Lap>
                <TotalTimeSeconds>100</TotalTimeSeconds>
                <Track>
                    <Trackpoint>
                        <Time>2018-04-15T07:00:00Z</Time>
                    </Trackpoint>
                </Track>
            </Lap>
        </Activity>
    </Activities>
</TrainingCenterDatabase>"""
    tcx_path = tmp_path / "no_hr.tcx"
    tcx_path.write_text(content)
    parser = TCXParser(str(tcx_path))
    assert parser.hr_max == 0
    assert parser.hr_min == 0
    assert parser.hr_avg == 0


def test_gpx_parser_no_heartrate(tmp_path):
    content = """<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1">
  <trk>
    <trkseg>
      <trkpt lat="60.17921760" lon="30.53807448">
        <time>2018-04-15T07:00:00Z</time>
      </trkpt>
    </trkseg>
  </trk>
</gpx>"""
    gpx_path = tmp_path / "no_hr.gpx"
    gpx_path.write_text(content)
    parser = GPXParser(str(gpx_path))
    assert parser.hr_max == 0
    assert parser.hr_min == 0
    assert parser.hr_avg == 0
