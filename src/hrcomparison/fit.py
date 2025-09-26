import contextlib
from datetime import datetime

import fitparse

from hrcomparison.base import ActivityParser


class FITParser(ActivityParser):
    """Parser for FIT files"""

    def _parse_file(self) -> None:  # noqa: C901
        self.fitfile = fitparse.FitFile(self.filename)

        self._time_values = []
        self._hr_values = []
        self._distance_values = []
        self._latitude = None
        self._longitude = None
        self._calories = 0
        self._activity_type = "other"

        # Get activity type from session message
        for session in self.fitfile.get_messages("session"):
            with contextlib.suppress(Exception):
                if sport := session.get_value("sport"):
                    self._activity_type = sport.lower()

            with contextlib.suppress(Exception):
                self._calories = session.get_value("total_calories", 0)

        # Get time series data from record messages
        for record in self.fitfile.get_messages("record"):
            try:
                if time_value := record.get_value("timestamp"):
                    self._time_values.append(time_value)

                    # Get heart rate
                    hr = record.get_value("heart_rate", 0)
                    self._hr_values.append(hr)

                    # Get distance
                    distance = record.get_value("distance", 0)
                    self._distance_values.append(distance)

                    # Get first position
                    if self._latitude is None:
                        self._latitude = record.get_value("position_lat")
                        if self._latitude is not None:
                            self._latitude = self._latitude * 180.0 / 2**31

                    if self._longitude is None:
                        self._longitude = record.get_value("position_long")
                        if self._longitude is not None:
                            self._longitude = self._longitude * 180.0 / 2**31

            except Exception:  # noqa: BLE001,S112
                continue

    @property
    def hr_values(self) -> list[int]:
        return self._hr_values

    @property
    def time_values(self) -> list[datetime]:
        return self._time_values

    @property
    def latitude(self) -> float | None:
        return self._latitude

    @property
    def longitude(self) -> float | None:
        return self._longitude

    @property
    def activity_type(self) -> str:
        return self._activity_type

    @property
    def completed_at(self) -> datetime:
        return self._time_values[-1] if self._time_values else datetime.now()

    @property
    def distance(self) -> float:
        return self._distance_values[-1] if self._distance_values else 0

    @property
    def duration(self) -> float:
        min_time_values_for_duration = 2  # Need at least start and end times

        if len(self._time_values) < min_time_values_for_duration:
            return 0

        start_time = self._time_values[0]
        end_time = self._time_values[-1]
        return (end_time - start_time).total_seconds()  # type: ignore

    @property
    def pace(self) -> list[float]:
        return self._distance_values

    @property
    def calories(self) -> float:
        return self._calories

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
