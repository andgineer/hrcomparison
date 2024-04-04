import time
from datetime import datetime
from typing import Optional, List

from lxml import objectify

namespace = "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"


class TCXParser:
    def __init__(self, tcx_file: str) -> None:
        tree = objectify.parse(tcx_file)  # pylint: disable=c-extension-no-member
        self.root = tree.getroot()
        self.activity = self.root.Activities.Activity
        self.time_values = []
        self.hr_values = []
        self.distance_values = []

        for lap in self.activity.Lap:
            for point in lap.Track.Trackpoint:
                if hasattr(point, "DistanceMeters"):
                    distance = float(point.DistanceMeters)
                else:
                    distance = 0
                self.distance_values.append(distance)
                time_spent = point.Time.text.split(".")[0].replace("Z", "")
                time_spent = datetime.strptime(time_spent, "%Y-%m-%dT%H:%M:%S")
                self.time_values.append(time_spent)
                hr = (
                    int(point.HeartRateBpm.Value)
                    if hasattr(point, "HeartRateBpm")
                    else 0
                )
                self.hr_values.append(hr)

    @property
    def latitude(self) -> Optional[float]:
        if hasattr(self.activity.Lap.Track.Trackpoint, "Position"):
            return self.activity.Lap.Track.Trackpoint.Position.LatitudeDegrees.pyval  # type: ignore
        return None

    @property
    def longitude(self) -> Optional[float]:
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
        return self.distance_values[-1]

    @property
    def distance_units(self) -> str:
        return "meters"

    @property
    def duration(self) -> float:
        """Returns duration of workout in seconds."""
        return sum(lap.TotalTimeSeconds for lap in self.activity.Lap)  # type: ignore

    @property
    def pace(self) -> List[float]:
        return self.distance_values

    @property
    def calories(self) -> float:
        return sum(lap.Calories for lap in self.activity.Lap)  # type: ignore

    @property
    def hr_avg(self) -> float:
        """Average heart rate of the workout"""
        hr_data = self.hr_values
        return sum(hr_data) / len(hr_data)

    @property
    def hr_max(self) -> float:
        """Maximum heart rate of the workout"""
        return max(self.hr_values)

    @property
    def hr_min(self) -> float:
        """Minimum heart rate of the workout"""
        return min(self.hr_values)

    @property
    def pace_avg(self) -> str:
        """Average pace (mm:ss/km for the workout"""
        secs_per_km = self.duration / (self.distance / 1000)
        return time.strftime("%M:%S", time.gmtime(secs_per_km))
