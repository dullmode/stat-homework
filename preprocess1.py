import pandas as pd
import numpy as np
from geopy import Nominatim, distance
from tqdm import tqdm


def get_zipcode(df, geolocator, lat_field, lon_field):
    location = geolocator.reverse((df[lat_field], df[lon_field]))
    if 'postcode' in location.raw['address']:
        return location.raw['address']['postcode']
    else:
        return np.nan

def get_min_distance_from_station(df, distance, lat_field, lon_field):
    best_km = None
    for i in st_df['the_geom']:
        i = i.split()
        st_lon = i[1][1:]
        st_lat = i[2][:-2]
        km = distance.distance(
                (df[lat_field], df[lon_field]),
                (st_lat, st_lon)
                )
        if best_km is None or km < best_km:
            best_km = km
    return best_km

tqdm.pandas()
ab_df = pd.read_csv("input_data/airbnb.csv")
hi_df = pd.read_csv("input_data/historic.csv")
st_df = pd.read_csv("input_data/station.csv")
cr_df = pd.read_csv("input_data/crime.csv")
geolocator = Nominatim(user_agent='http')

##adding column 'zip' using lat and lon to airbnb.csv
ab_df['zip'] = ab_df.progress_apply(
        get_zipcode,
        axis=1,
        geolocator=geolocator,
        lat_field='latitude',
        lon_field='longitude'
        )

#adding column 'dist_from_st' using lat and lon to airbnb.csv
ab_df['dist_from_st'] = ab_df.progress_apply(
        get_min_distance_from_station,
        axis=1,
        distance=distance,
        lat_field='latitude',
        lon_field='longitude'
        )
ab_df.to_csv('input_data/airbnb.csv')

##adding column 'zip' using lat and lon to historic.csv
hi_df['zip'] = hi_df.progress_apply(
        get_zipcode,
        axis=1,
        geolocator=geolocator,
        lat_field='Latitude',
        lon_field='Longitude'
        )
hi_df.to_csv('input_data/historic.csv')

#adding column 'zip' using lat and lon to crime.csv
cr_df = cr_df.sample(frac=0.1)
cr_df['zip'] = cr_df.progress_apply(
        get_zipcode,
        axis=1,
        geolocator=geolocator,
        lat_field='Latitude',
        lon_field='Longitude'
        )

cr_df.to_csv('input_data/crime.csv')

