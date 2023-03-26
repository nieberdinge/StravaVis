
from fit_tool.fit_file import FitFile

path = r"C:\Users\edthe\Projects\StravaVis\OMRC_It_stopped_raining_enough_for_me_to_get_up_and_go.gpx"
output_path = r"C:\Users\edthe\Projects\StravaVis\data.csv"

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from fit_tool.fit_file import FitFile
from fit_tool.profile.messages.record_message import RecordMessage


import gpxpy
import gpxpy.gpx
import pandas as pd
import geopy.distance
from numpy_ext import rolling_apply
import matplotlib.pyplot as plt

with open(path) as f:
    gpx = gpxpy.parse(f)

points = []
for segment in gpx.tracks[0].segments:
    for p in segment.points:
        points.append({
            'time': p.time,
            'latitude': p.latitude,
            'longitude': p.longitude,
            'elevation': p.elevation,
        })
df = pd.DataFrame.from_records(points)
coords = [(p.latitude, p.longitude) for p in df.itertuples()]
df['distance'] = [0] + [geopy.distance.distance(from_, to).m for from_, to in zip(coords[:-1], coords[1:])]
df['cumulative_distance'] = df.distance.cumsum()
df['duration'] = df.time.diff().dt.total_seconds().fillna(0)
df['cumulative_duration'] = df.duration.cumsum()
df['pace_metric'] = pd.Series((df.duration / 60) / (df.distance / 1000)).bfill()
print(df.head())



def rolling_metric_pace(duration, distance):
    return (duration.sum() / 60) / (distance.sum() / 1000)


x = df.cumulative_distance
y = rolling_apply(rolling_metric_pace, 10, df.duration.values, df.distance.values)

plt.plot(x, y)