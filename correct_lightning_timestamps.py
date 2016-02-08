"""Correct Lightning data back to UTC time for strikes before 2011-6-1

HiSPARC stations were using UTC time before that time.
Officially HiSPARC started using GPS time on 2010-3-8.
However, some stations were slower to adapt.

1306886400 2011-6-1 <- vanaf hier gebruikt HiSPARC duidelijk GPS tijd
1268006400 2010-3-8 <- vanaf hier zou HiSPARC GPS moeten gaan gebruiken

"""
import tables
import datetime
import time

with tables.open_file('/Users/reno/HiSPARC/Code/lightning/lightning_10km_120sec.h5', 'a') as data:
    data.remove_node('/lightning/corr_timestamps')

    t = data.root.lightning.timestamps.read()
    corr_t = []
    T = time.mktime(datetime.datetime(2011, 6, 1).utctimetuple())
    T13 = time.mktime(datetime.datetime(2006, 1, 1).utctimetuple())
    T14 = time.mktime(datetime.datetime(2009, 1, 1).utctimetuple())

    for u in t:
        if u < T:
            if u < T13:
                corr_t.append(u - 13)
            elif u < T14:
                corr_t.append(u - 14)
            else:
                corr_t.append(u - 15)
        else:
            corr_t.append(u)
    data.create_array('/lightning', 'corr_timestamps', corr_t)
