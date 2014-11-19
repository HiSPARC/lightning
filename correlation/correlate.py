import datetime

import hisparc_data
import knmi_lightning
import knmi_timestamps
import get_stations
import date_generator


def main():
    """Do the search for correlations between lightning strikes and events"""
    start = datetime.date(2011, 9, 10)
    stop = datetime.date(2011, 9, 10)
    station_ids = get_stations.get_station_ids(start)

    #  This should be in the for loop and start should be date.
    #  But for better performance, it is not yet..
    stations = get_stations.get_station_positions(station_ids, start)

    for date in date_generator.daterange(start, stop):
        lgt_file = knmi_lightning.data_file(date)
        his_file = hisparc_data.data_file(date)

        discharges = knmi_lightning.discharges(lgt_file)
        for discharge in discharges:
            matches = []
            close_station_ids = get_stations.find_close_stations(discharge, stations)
            for station_id in close_station_ids:
                events = hisparc_data.events_table(his_file, station_id)
                matched_events = hisparc_data.events_in_range(events, discharge['timestamp'])
                matches.append([station_id, matched_events['ext_timestamp']])
            if len(close_station_ids) > 0:
                print "Discharge:", discharge
                print "Close stations: ", close_station_ids
                print "Matching events: ", matches

        lgt_file.close()
        his_file.close()


if __name__=="__main__":
    main()
    print 'Done'
