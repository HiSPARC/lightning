import datetime
import operator
import os

import tables

import hisparc_data
import get_stations
import date_generator


TARGET_DIR = '/Users/arne/Datastore/timestamp_data'


def main():
    start = datetime.date(2011, 1, 1)
    stop = datetime.date(2011, 1, 10)
    for date in date_generator.daterange(start, stop):
        source_file = hisparc_data.data_file(date)
        if not source_file:
            continue
        target_file = get_target_file(date)
        for events in source_file.walkNodes('/', 'Table'):
            if not events.name == 'events':
                continue
            target_table = target_file.createTable(
                    os.path.split(events._v_pathname)[0], 'events',
                    EventTimestamps, createparents=True)
            event_id = events.col('event_id')
            ext_timestamps = events.col('ext_timestamp')
            timestamps = events.col('timestamp')
            nanoseconds = events.col('nanoseconds')
            rows_data = zip(event_id, ext_timestamps, timestamps, nanoseconds)
            for row_data in rows_data:
                row = target_table.row
                row['event_id'] = row_data[0]
                row['ext_timestamp'] = row_data[1]
                row['timestamp'] = row_data[2]
                row['nanoseconds'] = row_data[3]
                row.append()
            target_table.flush()
            clean_events_table(target_file, target_table)
        source_file.close()
        target_file.close()


def get_target_file(date, rootdir=TARGET_DIR):
    fullpath = hisparc_data.data_path(date, rootdir)
    splitpath = os.path.split(fullpath)
    path = splitpath[0]
    filename = splitpath[1]
    create_path(path)
    file = tables.openFile(fullpath, 'w')
    return file


def create_path(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


def clean_events_table(datafile, events_table):
    """Clean the events table.

    Remove duplicate events and sort the table by ext_timestamp.

    """
    events_tablename = events_table.name

    enumerated_timestamps = list(enumerate(events_table.col('ext_timestamp')))
    enumerated_timestamps.sort(key=operator.itemgetter(1))

    unique_sorted_ids = _find_unique_row_ids(enumerated_timestamps)
    new_events = _replace_table_with_selected_rows(datafile, events_table,
                                                   unique_sorted_ids)
    _normalize_event_ids(new_events)


def _find_unique_row_ids(enumerated_timestamps):
    """Find the unique row_ids from sorted enumerated timestamps."""

    prev_timestamp = 0
    unique_sorted_ids = []
    for row_id, timestamp in enumerated_timestamps:
        if timestamp != prev_timestamp:
            # event is unique, so add it
            unique_sorted_ids.append(row_id)
        prev_timestamp = timestamp

    return unique_sorted_ids


def _replace_table_with_selected_rows(datafile, events_table, row_ids):
    """Replace events table with selected rows.

    :param events_table: original events table to be replaced.
    :param row_ids: row ids of the selected rows which should go in
        the destination table.

    """
    tmptable = datafile.createTable(os.path.split(events_table._v_pathname)[0],
                                    't__events',
                                    description=events_table.description)
    selected_rows = events_table.readCoordinates(row_ids)
    tmptable.append(selected_rows)
    tmptable.flush()
    datafile.renameNode(tmptable, events_table.name, overwrite=True)
    return tmptable


def _normalize_event_ids(events):
    """Normalize event ids.

    After sorting, the event ids no longer correspond to the row
    number.  This can complicate finding the row id of a particular
    event.  This method will replace the event_ids of all events by
    the row id.

    :param events: the events table to normalize.

    """
    row_ids = range(len(events))
    events.modifyColumn(column=row_ids, colname='event_id')


class EventTimestamps(tables.IsDescription):
    """Store event timestamps.

    """
    event_id = tables.UInt32Col()
    timestamp = tables.Time32Col()
    nanoseconds = tables.UInt32Col()
    ext_timestamp = tables.UInt64Col()


if __name__=="__main__":
    main()
    print 'Done'
