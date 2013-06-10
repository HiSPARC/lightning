from urllib2 import urlopen, HTTPError, URLError
import json

import numpy as np


api_base = 'http://data.hisparc.nl/api/'


def find_close_stations(point, stations, radius=3000):
    ids = np.array([station['station_id'] for station in stations])
    lat = np.array([station['latitude'] for station in stations])
    lon = np.array([station['longitude'] for station in stations])

    distances = distance_coordinates(point['latitude'], point['longitude'],
                                     lat, lon)

    close = ids[np.where(distances < radius)]

    return close


def distance_coordinates(lat1, lon1, lat2, lon2):
    R = 6371000  # [m] Radius of earth
    dLat = np.radians(lat2 - lat1)
    dLon = np.radians(lon2 - lon1)
    a = (np.sin(dLat / 2) ** 2 + np.cos(np.radians(lat1)) *
         np.cos(np.radians(lat2)) * np.sin(dLon / 2) ** 2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c

    return distance


def get_station_positions(station_ids, date=None):
    url = api_base + 'station/%d/config/'
    if date:
        url += date.strftime('%Y/%-m/%-d/')
    positions = []
    for station_id in station_ids:
        try:
            config = json.loads(urlopen(url % station_id).read())
        except HTTPError:
            continue
        positions.append({'station_id': station_id,
                          'latitude': config['gps_latitude'],
                          'longitude': config['gps_longitude']})
    return positions


def get_station_ids():
    stations = json.loads(urlopen(api_base + 'stations/').read())

    return [station['number'] for station in stations]


def test_501():
    """Get Science Park stations"""
    point = {'latitude': 52.3559285618, 'longitude': 4.95114426884}
    station_ids = get_station_ids()
    station_positions = get_station_positions(station_ids)
    close_stations = find_close_stations(point, station_positions, radius=1000)

    return close_stations
