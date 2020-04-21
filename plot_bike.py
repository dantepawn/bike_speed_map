import pandas as pd
import numpy as np
import gpxpy
#import argparser

import glob
import folium
from branca.colormap import linear



gpx_files = glob.glob('C:/Users/daeil/Documents/bike/data/*.gpx')
csv_files = glob.glob('C:/Users/daeil/Documents/bike/data/*.csv')


def extract_segments(gpx_file):
    gpx_file = open(gpx_file, 'r')
    gpx = gpxpy.parse(gpx_file)
    lat = []
    lon = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)
    segments = list(zip(lat, lon))

    return segments

def create_df(csv_file):
    alles = pd.read_csv(csv_file,header=0)
    general_stats = alles.iloc[0,:]
    df = pd.DataFrame(alles.iloc[2:,:].values, columns = alles.iloc[1,:] )
    ZEROS = df[df['Distances (m)'].apply(lambda x : float(x) == 0)].shape[0]
    df = df[df['Distances (m)'].apply(lambda x : float(x)  ) > 0]
    return df , general_stats , ZEROS


def plot_speed(gpx_file, csv_file):
    ''' must include ZEROS in the plotting!! '''
    segments = extract_segments(gpx_file)
    df, stats, zeros = create_df(csv_file)
    speed = df['Speed (km/h)'].map(float)
    rolling_ave = np.convolve(speed, np.ones((10,)) / 10, mode='valid')


    centerY = np.mean([c[0] for c in segments])
    centerX = np.mean([c[1] for c in segments])

    min_col = rolling_ave.min()
    max_col = rolling_ave.max()

    colormap = linear.viridis.scale(min_col, max_col)



    base = folium.Map(location=(centerY, centerX), tiles='cartoDBpositron', width='100%', height='100%')

    folium.ColorLine(
        positions=segments,
        colors=rolling_ave,
        colormap=colormap,
        weight=4
    ).add_to(base)

    colormap.caption = 'Km/h'
    colormap.add_to(base)


    return base

gpx_file = gpx_files[-1]
csv_file = csv_files[-1]

base = plot_speed(gpx_file, csv_file)
base.save('outputmap.html')

# to create the color map

