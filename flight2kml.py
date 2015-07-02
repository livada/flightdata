from kml import KMLDocument, KMLTrack

with open('Flt0508_20150611F_2.csv') as f:
    info = {}
    header = None
    data = []
    reading_info = True
    for l in f.readlines():
	line = l.strip().split(',')
        if reading_info:
            if line[0] == 'TIME':
                header = line
                reading_info = False
            else:
                infoline = map(str.strip, l.split(':', 1))
                info[infoline[0].strip('.')] = infoline[1] if len(infoline)>1 else ''
        else:
            data.append(line)

indices = dict([(k, v) for v, k in enumerate(header)])

# print info
# print header
# print data[:10]
# print indices

track = KMLTrack('Example track') #, altitude_mode='absolute')

SHOWING_KEYWORDS = 'FUEL oil RPM'.split()
showing_indices = sorted([i for k, i in indices.iteritems() if any([(key.lower() in k.lower()) for key in SHOWING_KEYWORDS])])

# print [header[i] for i in showing]

CARDINAL_POINTS = {'N': 1, 'E': 1, 'W': -1, 'S': -1}

def deg(val, coord_type='C DDD MM.MMM'):
    if coord_type=='C DDD MM.MMM':
        val = val.split()
        if val[0] not in CARDINAL_POINTS.keys():
            return None
        return CARDINAL_POINTS[val[0]] * (float(val[1]) + float(val[2]) / 60)


localtime_date = info['Local Time'].split()[0].replace('/','-')

for d in data:
    time = '%(date)sT%(time)s' % {
                                   'date': localtime_date,
                                   'time': d[indices['TIME']]
                                  }
    lat = deg(d[indices['Latitude']])
    lon = deg(d[indices['Longitude']])
    alt = 0.0

    core = (time, lat, lon, alt)

    if None in core:
        continue # Skip frames with unvalid coordinates

    ext = dict([(header[i], d[i]) for i in showing_indices])
    
    track.add(*core, **ext)

# print track

doc = KMLDocument('Flight Data Recording')
doc.objects.append(track)

print doc
