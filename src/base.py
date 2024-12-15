import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional


class ActivityParser(ABC):
    """Abstract base class for parsing activity files"""

    def __init__(self, filename: str):
        self.filename = filename
        self._parse_file()

    @abstractmethod
    def _parse_file(self) -> None:
        """Parse the activity file and store the data"""

    @property
    @abstractmethod
    def hr_values(self) -> List[int]:
        """Get heart rate values"""

    @property
    @abstractmethod
    def time_values(self) -> List[datetime]:
        """Get time values"""

    @property
    @abstractmethod
    def hr_max(self) -> float:
        """Maximum heart rate of the workout"""

    @property
    @abstractmethod
    def hr_min(self) -> float:
        """Minimum heart rate of the workout"""

    @property
    @abstractmethod
    def hr_avg(self) -> float:
        """Average heart rate of the workout"""

    @property
    @abstractmethod
    def distance(self) -> float:
        """Total distance in meters"""

    @property
    @abstractmethod
    def duration(self) -> float:
        """Duration in seconds"""

    @property
    @abstractmethod
    def latitude(self) -> Optional[float]:
        """Starting latitude"""

    @property
    @abstractmethod
    def longitude(self) -> Optional[float]:
        """Starting longitude"""

    @property
    @abstractmethod
    def pace(self) -> List[float]:
        """List of pace values"""

    @property
    @abstractmethod
    def calories(self) -> float:
        """Total calories burned"""

    @property
    @abstractmethod
    def completed_at(self) -> datetime:
        """Completion time"""

    @property
    @abstractmethod
    def activity_type(self) -> str:
        """Type of activity"""

    @property
    def distance_units(self) -> str:
        """Distance units (always meters)"""
        return "meters"

    @property
    def pace_avg(self) -> str:
        """Average pace (mm:ss/km)"""
        if self.distance == 0:
            return "00:00"
        secs_per_km = self.duration / (self.distance / 1000)
        return time.strftime("%M:%S", time.gmtime(secs_per_km))
