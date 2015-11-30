from urllib2 import urlopen, HTTPError, URLError
import json

import numpy as np

from sapphire import Network, Station


api_base = 'http://data.hisparc.nl/api/'


def find_close_stations(point, stations, radius=3000):
    """Get stations close to a point

    :param point: longitude and latitude close to which stations should be
        found.
    :param stations: list of dictionaries with station number and position
    :param radius: the maximum distance from the point for stations to be
        considered close.

    :return: list of station ids that are within radius of the point.

    """
    ids = np.array([station_id for station_id in stations.keys()])
    lat = np.array([station['latitude'] for station in stations.values()])
    lon = np.array([station['longitude'] for station in stations.values()])

    distances = distance_coordinates(point['latitude'], point['longitude'],
                                     lat, lon)

    close = ids[np.where(distances < radius)]

    return close


def distance_coordinates(latitude1, longitude1, latitude2, longitude2):
    """Calculate distance between two coordinates

    :return: distance between points
    """
    R = 6371000  # [m] Radius of earth
    dLat = np.radians(latitude2 - latitude1)
    dLon = np.radians(longitude2 - longitude1)
    a = (np.sin(dLat / 2) ** 2 + np.cos(np.radians(latitude1)) *
         np.cos(np.radians(latitude2)) * np.sin(dLon / 2) ** 2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c

    return distance


def get_station_positions():
    """Get the positions of all stations."""

    net = {}
    for s in Network().station_numbers():
        try:
            station = Station(s)
            station.gps_locations
            net[s] = station
        except:
            pass
    return net


def get_station_position_for_timestamp(timestamp, stations):
    """Get the position of all stations for a specific timestamp.

    :param timestamp: unix timestamp in GPS
    :param stations: dictionary of station objects, with the station number as
                     the keys

    """
    return {s: u.gps_location(timestamp) for s, u in stations.iteritems()}


def get_station_ids(date=None):
    """Using API get all stations that have data on date

    :param date: date for which stations should have data
    """
    if date:
        url = api_base + 'stations/data/'
        url += date.strftime('%Y/%-m/%-d/')
        stations = json.loads(urlopen(url).read())
    else:
        stations = json.loads(urlopen(api_base + 'stations/').read())

    return [station['number'] for station in stations]


def test_501():
    """Get Science Park stations, close to 501"""
    point = {'latitude': 52.3559285618, 'longitude': 4.95114426884}
    station_ids = get_station_ids()
    station_positions = get_station_positions(station_ids)
    close_stations = find_close_stations(point, station_positions, radius=1000)

    return close_stations
