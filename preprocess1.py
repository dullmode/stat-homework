import pandas as pd
import numpy as np
import geopy


def get_zipcode(df, geolocator, lat_field, lon_field):
    print(df[lat_field], df[lon_field])
    location = geolocator.reverse((df[lat_field], df[lon_field]))
    if 'postcode' in location.raw['address']:
        return location.raw['address']['postcode']
    else:
        return np.nan

df = pd.read_csv("input_data/airbnb.csv")

geolocator = geopy.Nominatim(user_agent='http')

#adding column 'zip' using lat and lon
df['zip'] = df.apply(
        get_zipcode,
        axis=1,
        geolocator=geolocator,
        lat_field='latitude',
        lon_field='longitude'
        )

df.to_csv('input_data/airbnb.csv')
