from datetime import datetime

import gpxpy

from hrcomparison.base import ActivityParser


class GPXParser(ActivityParser):
    """Parser for GPX files"""

    def _parse_file(self) -> None:
        with open(self.filename, encoding="utf8") as gpx_file:
            self.gpx = gpxpy.parse(gpx_file)

        self._time_values = []
        self._hr_values = []
        self._distance_values: list[float] = []
        self._durations: list[float] = []

        for track in self.gpx.tracks:
            for segment in track.segments:
                for i, point in enumerate(segment.points):
                    self._time_values.append(point.time)

                    # Calculate distance
                    if i > 0:
                        assert self._distance_values
                        dist = point.distance_2d(segment.points[i - 1])
                        assert dist
                        self._distance_values.append(self._distance_values[-1] + dist)
                    else:
                        self._distance_values.append(0.0)

                    # Get heart rate from extensions
                    hr = 0
                    for extension in point.extensions:
                        ns = "{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}"
                        hr_elem = extension.find(f"{ns}hr")
                        if hr_elem is not None:
                            hr = int(hr_elem.text)
                            break
                    self._hr_values.append(hr)

    @property
    def hr_values(self) -> list[int]:
        return self._hr_values

    @property
    def time_values(self) -> list[datetime]:
        return self._time_values  # type: ignore

    @property
    def latitude(self) -> float | None:
        if self.gpx.tracks and self.gpx.tracks[0].segments:
            return self.gpx.tracks[0].segments[0].points[0].latitude
        return None

    @property
    def longitude(self) -> float | None:
        if self.gpx.tracks and self.gpx.tracks[0].segments:
            return self.gpx.tracks[0].segments[0].points[0].longitude
        return None

    @property
    def activity_type(self) -> str:
        return "other"  # GPX doesn't typically specify activity type

    @property
    def completed_at(self) -> datetime:
        return self._time_values[-1] if self._time_values else datetime.now()  # type: ignore

    @property
    def distance(self) -> float:
        return self._distance_values[-1] if self._distance_values else 0

    @property
    def duration(self) -> float:
        min_time_values_for_duration = 2  # Need at least start and end times
        if not self._time_values or len(self._time_values) < min_time_values_for_duration:
            return 0

        # Filter out None values and get first and last valid timestamps
        valid_times = [t for t in self._time_values if t is not None]
        if len(valid_times) < min_time_values_for_duration:
            return 0

        return (valid_times[-1] - valid_times[0]).total_seconds()

    @property
    def pace(self) -> list[float]:
        return self._distance_values

    @property
    def calories(self) -> float:
        return 0  # GPX doesn't typically include calorie data

    @property
    def hr_avg(self) -> float:
        hr_data = [x for x in self._hr_values if x > 0]
        return sum(hr_data) / len(hr_data) if hr_data else 0

    @property
    def hr_max(self) -> float:
        return max(self._hr_values) if self._hr_values else 0

    @property
    def hr_min(self) -> float:
        hr_data = [x for x in self._hr_values if x > 0]
        return min(hr_data) if hr_data else 0
