import tables
import sapphire

data = tables.open_file('/Users/reno/HiSPARC/Code/lightning/lightning_10km.h5', 'r')

timestamps = data.root.lightning.timestamps
nanoseconds = data.root.lightning.nanoseconds
n_stations = data.root.lightning.n_stations
stations = data.root.lightning.stations

nrows = data.root.lightning.timestamps.nrows

dts = [] # lege lijst met tijdverschillen dt

ndts = 0

for i in sapphire.utils.pbar(xrange(nrows)):
    statname = ['/s%s' % u for u in stations[i].split(',')]
    litime = timestamps[i]
    linano = nanoseconds[i]*1e-9
    for j in xrange(len(statname)):
        ev = data.get_node(statname[j], 'events')
        evtimecol = ev.col('timestamp')
        nanoseccol = ev.col('nanoseconds')*1e-9
        diftime = evtimecol - litime + nanoseccol - linano

        filter14 = (abs(diftime + 14) < 0.0002)
        filter13 = (abs(diftime + 13) < 0.0002)
        filter0 = (abs(diftime) < 0.0002)
        filters = filter14 & filter13 & filter0
        ev.read_where(filters)

        dt = diftime.compress(filters)
        dts.extend(dt)
