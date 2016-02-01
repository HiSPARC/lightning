import csv

import tables

from sapphire import esd, time_util


def download_data_for_stations(timestamp, stations):
    t0 = time_util.GPSTime(timestamp - 60).datetime()
    t1 = time_util.GPSTime(timestamp + 60).datetime()
    
    print "Downloading data from %s to %s for stations %s" % (t0, t1, stations)
    
    for station in stations:
        esd.download_data(data, '/s%d' % station, station, start=t0, end=t1)


if __name__ == '__main__':
    data = tables.open_file('lightning_10km.h5', 'w')
    
    with open('lightning_10km.csv') as f:        
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            timestamp = int(line[0])
            station_string = line[-1]
            stations = [int(u) for u in station_string.split(',')]
            
            download_data_for_stations(timestamp, stations)