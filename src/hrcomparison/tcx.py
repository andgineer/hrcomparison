from datetime import datetime

from lxml import objectify

from hrcomparison.base import ActivityParser


class TCXParser(ActivityParser):
    """Parser for TCX files"""

    def _parse_file(self) -> None:
        tree = objectify.parse(self.filename)  # pylint: disable=c-extension-no-member
        self.root = tree.getroot()
        self.activity = self.root.Activities.Activity
        self._time_values = []
        self._hr_values = []
        self._distance_values = []

        for lap in self.activity.Lap:
            for point in lap.Track.Trackpoint:
                if hasattr(point, "HeartRateBpm"):
                    distance = (
                        float(point.DistanceMeters) if hasattr(point, "DistanceMeters") else 0
                    )
                    self._distance_values.append(distance)
                    time_str = point.Time.text.split(".")[0].replace("Z", "")
                    time_spent = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
                    self._time_values.append(time_spent)
                    hr = int(point.HeartRateBpm.Value)
                    self._hr_values.append(hr)

    @property
    def hr_values(self) -> list[int]:
        return self._hr_values

    @property
    def time_values(self) -> list[datetime]:
        return self._time_values

    @property
    def latitude(self) -> float | None:
        if hasattr(self.activity.Lap.Track.Trackpoint, "Position"):
            return self.activity.Lap.Track.Trackpoint.Position.LatitudeDegrees.pyval  # type: ignore
        return None

    @property
    def longitude(self) -> float | None:
        if hasattr(self.activity.Lap.Track.Trackpoint, "Position"):
            return self.activity.Lap.Track.Trackpoint.Position.LongitudeDegrees.pyval  # type: ignore
        return None

    @property
    def activity_type(self) -> str:
        return self.activity.attrib["Sport"].lower()  # type: ignore

    @property
    def completed_at(self) -> datetime:
        return self.activity.Lap[-1].Track.Trackpoint[-1].Time.pyval  # type: ignore

    @property
    def distance(self) -> float:
        return self._distance_values[-1] if self._distance_values else 0

    @property
    def duration(self) -> float:
        return sum(lap.TotalTimeSeconds for lap in self.activity.Lap)  # type: ignore

    @property
    def pace(self) -> list[float]:
        return self._distance_values

    @property
    def calories(self) -> float:
        return sum(lap.Calories for lap in self.activity.Lap)  # type: ignore

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
