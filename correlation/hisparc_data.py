import os
import urllib2
import json

import tables


DATA_PATH = "/Users/Matthijs/HiSPARC/Datastore/HiSPARC/"
api_base = 'http://data.hisparc.nl/api/'


def events_in_range(events, start, end=None):
    """Return the events table

    :param events: the event table for the station
    :param start: start timestamp
    :param end: end timestamp

    :return: events that fall within the time range

    """
    if not end:
        end = start + 1
    close_events = events.readWhere('(start <= timestamp) & (timestamp < end)')

    return close_events


def events_table(file, station_id):
    """Return the events table

    :param file: PyTable instance of the data file
    :param station_id: the id of the station

    :return: the event table for the station

    """
    url = api_base + 'station/%d/' % station_id
    station_info = json.loads(urllib2.urlopen(url).read())
    cluster = station_info['cluster']
    group_path = '/hisparc/cluster_%s/station_%d' % (cluster.lower(), station_id)
    events = file.getNode(group_path, 'events')

    return events


def data_file(date):
    """Return PyTables data file

    :param date: the date as a datetime.date object

    :return: PyTables instance of the data file

    """
    filepath = data_path(date)
    try:
        file = tables.openFile(filepath, 'r')
    except IOError:
        print "No data for %s." % date.strftime('%Y_%-m_%-d')

    return file


def data_path(date):
    """Return path to HiSPARC data file

    Return path to the HiSPARC data file of a particular date

    :param date: the date as a datetime.date object

    :return: path to the HiSPARC data file

    """
    rootdir = DATA_PATH
    filepath = date.strftime('%Y/%-m/%Y_%-m_%-d.h5')

    return os.path.join(rootdir, filepath)
