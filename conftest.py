"""
Tests run from the project root folder.
But the python code expects to run inside server folder.

So for tests we add server folder to sys.path.

This file is loaded first by py.test therefore we change sys.path for all other python files.
"""

import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from datetime import datetime

import pytest


@pytest.fixture
def sample_tcx_content():
    return """<?xml version="1.0" encoding="UTF-8"?>
<TrainingCenterDatabase xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2">
    <Activities>
        <Activity Sport="Other">
            <Lap>
                <TotalTimeSeconds>6238.0</TotalTimeSeconds>
                <DistanceMeters>17524.94921875</DistanceMeters>
                <Calories>797</Calories>
                <Track>
                    <Trackpoint>
                        <Time>2018-04-15T07:00:00.000Z</Time>
                        <Position>
                            <LatitudeDegrees>60.17921760678291</LatitudeDegrees>
                            <LongitudeDegrees>30.538074485957623</LongitudeDegrees>
                        </Position>
                        <HeartRateBpm>
                            <Value>59</Value>
                        </HeartRateBpm>
                        <DistanceMeters>0</DistanceMeters>
                    </Trackpoint>
                    <Trackpoint>
                        <Time>2018-04-15T07:45:02.000Z</Time>
                        <HeartRateBpm>
                            <Value>160</Value>
                        </HeartRateBpm>
                        <DistanceMeters>17524.94921875</DistanceMeters>
                    </Trackpoint>
                </Track>
            </Lap>
        </Activity>
    </Activities>
</TrainingCenterDatabase>"""


@pytest.fixture
def tcx_file(tmp_path, sample_tcx_content):
    tcx_path = tmp_path / "test.tcx"
    tcx_path.write_text(sample_tcx_content)
    return str(tcx_path)


@pytest.fixture
def sample_gpx_content():
    return """<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="Garmin Connect API">
  <trk>
    <trkseg>
      <trkpt lat="60.17921760" lon="30.53807448">
        <ele>1234</ele>
        <time>2018-04-15T07:00:00Z</time>
        <extensions>
          <gpxtpx:TrackPointExtension xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1">
            <gpxtpx:hr>140</gpxtpx:hr>
          </gpxtpx:TrackPointExtension>
        </extensions>
      </trkpt>
      <trkpt lat="60.17922760" lon="30.53808448">
        <ele>1235</ele>
        <time>2018-04-15T07:00:10Z</time>
        <extensions>
          <gpxtpx:TrackPointExtension xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1">
            <gpxtpx:hr>145</gpxtpx:hr>
          </gpxtpx:TrackPointExtension>
        </extensions>
      </trkpt>
    </trkseg>
  </trk>
</gpx>"""


@pytest.fixture
def gpx_file(tmp_path, sample_gpx_content):
    gpx_path = tmp_path / "test.gpx"
    gpx_path.write_text(sample_gpx_content)
    return str(gpx_path)


@pytest.fixture
def mock_fit_messages():
    from unittest.mock import MagicMock

    session_message = MagicMock()
    session_message.get_value.side_effect = lambda field, default=None: {
        "sport": "running",
        "total_calories": 500,
    }.get(field, default)

    # Create message records with proper heart rate sequencing
    record_messages = []
    for i in range(3):
        message = MagicMock()
        values = {
            "timestamp": datetime(2018, 4, 15, 7, 0, i),
            "heart_rate": 140 + i,
            "distance": i * 100,
            "position_lat": int(60.17921760 * (2**31) / 180) if i == 0 else None,
            "position_long": int(30.53807448 * (2**31) / 180) if i == 0 else None,
        }

        # Create a closure to capture the current values
        def make_get_value(stored_values):
            def get_value(field, default=None):
                return stored_values.get(field, default)

            return get_value

        message.get_value = make_get_value(values)
        record_messages.append(message)

    return {"session": [session_message], "record": record_messages}


@pytest.fixture
def fit_file(tmp_path, mock_fit_messages):
    from unittest.mock import patch

    fit_path = tmp_path / "test.fit"
    fit_path.touch()

    # Create a class to mock FitFile
    class MockFitFile:
        def get_messages(self, message_type):
            return mock_fit_messages[message_type]

    with patch("fitparse.FitFile", return_value=MockFitFile()):
        yield str(fit_path)
