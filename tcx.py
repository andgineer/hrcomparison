import time
from datetime import datetime
from lxml import objectify

namespace = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'


class TCXParser:

    def __init__(self, tcx_file):
        tree = objectify.parse(tcx_file)
        self.root = tree.getroot()
        self.activity = self.root.Activities.Activity
        self.time_values = []
        self.hr_values = []
        self.distance_values = []

        for lap in self.activity.Lap:
            for point in lap.Track.Trackpoint:
                if hasattr(point, 'DistanceMeters'):
                    distance = float(point.DistanceMeters)
                else:
                    distance = 0
                self.distance_values.append(distance)
                time_spent = point.Time.text.split('.')[0].replace('Z', '')
                time_spent = datetime.strptime(time_spent, '%Y-%m-%dT%H:%M:%S')
                self.time_values.append(time_spent)
                if hasattr(point, 'HeartRateBpm'):
                    hr = int(point.HeartRateBpm.Value)
                else:
                    hr = 0
                self.hr_values.append(hr)

    @property
    def latitude(self):
        if hasattr(self.activity.Lap.Track.Trackpoint, 'Position'):
            return self.activity.Lap.Track.Trackpoint.Position.LatitudeDegrees.pyval

    @property
    def longitude(self):
        if hasattr(self.activity.Lap.Track.Trackpoint, 'Position'):
            return self.activity.Lap.Track.Trackpoint.Position.LongitudeDegrees.pyval

    @property
    def activity_type(self):
        return self.activity.attrib['Sport'].lower()

    @property
    def completed_at(self):
        return self.activity.Lap[-1].Track.Trackpoint[-1].Time.pyval

    @property
    def cadence_avg(self):
        return self.activity.Lap[-1].Cadence

    @property
    def distance(self):
        return self.distance_values[-1]

    @property
    def distance_units(self):
        return 'meters'

    @property
    def duration(self):
        """Returns duration of workout in seconds."""
        return sum(lap.TotalTimeSeconds for lap in self.activity.Lap)

    @property
    def pace(self):
        return self.distance_values

    @property
    def calories(self):
        return sum(lap.Calories for lap in self.activity.Lap)

    @property
    def hr_avg(self):
        """Average heart rate of the workout"""
        hr_data = self.hr_values
        return sum(hr_data)/len(hr_data)

    @property
    def hr_max(self):
        """Maximum heart rate of the workout"""
        return max(self.hr_values)

    @property
    def hr_min(self):
        """Minimum heart rate of the workout"""
        return min(self.hr_values)

    @property
    def pace_avg(self):
        """Average pace (mm:ss/km for the workout"""
        secs_per_km = self.duration/(self.distance/1000)
        return time.strftime('%M:%S', time.gmtime(secs_per_km))


if __name__ == "__main__":
    tcx = TCXParser('/home/sorokin/Downloads/20180425_run_garmin.tcx')
    print(tcx.hr_max)