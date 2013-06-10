import datetime

import hisparc_data
import knmi_lightning
import knmi_timestamps
import get_close_stations


def main():

    start = datetime.date(2011, 9, 10)
    stop = datetime.date(2011, 9, 10)
    station_ids = get_close_stations.get_station_ids(start)

    #  This should be in the for loop and start should be date.
    #  But for better performance, it is not yet..
    stations = get_close_stations.get_station_positions(station_ids, start)

    for date in daterange(start, stop):
        lgt_file = knmi_lightning.data_file(date)
        his_file = hisparc_data.data_file(date)

        discharges = knmi_lightning.discharges(lgt_file)
        for discharge in discharges:
            matches = []
            close_station_ids = get_close_stations.find_close_stations(discharge, stations)
            for station_id in close_station_ids:
                events = hisparc_data.events_table(his_file, station_id)
                matched_events = hisparc_data.events_in_range(events, discharge['timestamp'])
                matches.append([station_id, matched_events])
            if len(close_station_ids) > 0:
                print "Discharge:", discharge
                print "Close stations: ", close_station_ids
                print "Matching events: ", matches

        lgt_file.close()
        his_file.close()


def daterange(start, stop):
    """Generator for date ranges

    This is a generator for date ranges.  Based on a start and stop value,
    it generates one day intervals.

    :param start: a date instance
    :param stop: a date instance

    :yield date: one day intervals between start and stop
    """
    if start == stop:
        yield start
        return
    else:
        yield start
        cur = start
        while cur < stop:
            cur += datetime.timedelta(days=1)
            yield cur
        return


if __name__=="__main__":
    main()
    print 'Done'
