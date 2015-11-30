import os
from datetime import timedelta

import tables
import numpy as np

import knmi_timestamps


LGT_PATH = "/Users/arne/Datastore/Lightning/"


def discharges(date, type=4):
    """Get discharge information for discharges of certain type

    :param date: the date as a datetime.date object
    :param type: the type of detected event (default: 4, cloud-ground)

    :return: arrays time_offset, latitude, longitude for events of chosen type

    """
    # FIXME: Might be a discharge2, check this.
    file = data_file(date)
    discharge_table = file.getNode('/discharge1')
    cg_idx = np.where(discharge_table.event_type[:] == type)


    discharges = [{'timestamp': knmi_timestamps.get_gps_timestamp(file,
                                            discharge_table.time_offset[idx])[0],
                   'nanoseconds': knmi_timestamps.get_gps_timestamp(file,
                                            discharge_table.time_offset[idx])[1],
                   'latitude': discharge_table.latitude[idx],
                   'longitude': discharge_table.longitude[idx]}
                  for idx in cg_idx[0]]

    return discharges


def data_file(date):
    """Return PyTables data file

    :param date: the date as a datetime.date object

    :return: PyTables instance of the data file

    """
    filepath = data_path(date)
    try:
        file = tables.openFile(filepath, 'r')
    except IOError:
        print "No datefile for %s." % date.strftime('%Y_%-m_%-d')
        raise
    return file


def data_path(date):
    """Return path to KNMI LGT file

    Return path to the KNMI LGT file of a particular date
    Note that 1 day is added to the file name, because KNMI names the files
    for the end date of the data.

    :param date: the date as a datetime.date object

    :return: path to the KNMI LGT file

    """
    rootdir = LGT_PATH
    date += timedelta(days=1)
    filepath = date.strftime('%Y/%-m/%Y_%-m_%-d.h5')

    return os.path.join(rootdir, filepath)
