class KMLException(Exception): pass

DOCUMENT = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"
 xmlns:gx="http://www.google.com/kml/ext/2.2">

  <Document>
    <name>%(name)s</name>
      <Style id="trackdefault">
        <LineStyle>
          <color>ff005dff</color>
          <width>5</width>
        </LineStyle>
      </Style>

%(objects)s

  </Document>
</kml>
'''

class KMLDocument:
    def __init__(self, name='Noname'):
        self.name = name
        self.objects = []

    def __str__(self):
        return DOCUMENT % {
                           'name': self.name,
                           'objects': '\n'.join(map(str, self.objects))
                          }


TRACK = '''
%(schema)s
      <Placemark>
        <name>%(name)s</name>
	<styleUrl>#trackdefault</styleUrl>
        <gx:Track>
          <altitudeMode>%(altitudeMode)s</altitudeMode>
%(times)s
%(coords)s
%(extendedData)s
        </gx:Track>
      </Placemark>
'''

TRACK_TIME = '          <when>%s</when>'
TRACK_COORD = '          <gx:coord>%s</gx:coord>'

SCHEMA = '''      <Schema id="schema">
%(fields)s
      </Schema>
'''
SCHEMA_FIELD = '''        <gx:SimpleArrayField name="%(name)s" type="%(type)s">
          <displayName>%(caption)s</displayName>
        </gx:SimpleArrayField>
'''

EXTENDED_DATA = '''          <ExtendedData>
            <SchemaData schemaUrl="#schema">
%(arrays)s
            </SchemaData>
          </ExtendedData>
'''

EXTENDED_DATA_ARRAY = '''
              <gx:SimpleArrayData name="%(name)s">
%(values)s
              </gx:SimpleArrayData>
'''

EXTENDED_DATA_VALUE = '                <gx:value>%s</gx:value>'



class KMLTrack:
    def __init__(self, name, altitude_mode=None):
        self.name = name

        self.altitude_mode = 'clampToGround'if altitude_mode is None else altitude_mode
        # clampToGround, relativeToGround, or absolute

        self.times = []
        self.coords = []
        self.extended_data = {}

    def add(self, time, lat, lon, alt=None, **kw):
        self.times.append(time)
        self.coords.append(self.pack_coord(lat, lon, alt))
        for k, v in kw.iteritems():
            if k not in self.extended_data:
                 self.extended_data[k] = ['n/a'] * (len(self.times) - 1)
            self.extended_data[k].append(v)

    def pack_coord(self, lat, lon, alt=None):
        if not all(map(lambda v: type(v) in (int, float), (lat, lon))):
            raise KMLException('Must provide valid latitude and longitude')
        coord = ['{:.6f}'.format(v) for v in (lon, lat, alt) if v is not None]
        return ' '.join(coord)

    def format_times(self):
        return '\n'.join([TRACK_TIME % str(t) for t in self.times])

    def format_coords(self):
        return '\n'.join([TRACK_COORD % str(c) for c in self.coords])

    def format_schema(self):
        if len(self.extended_data) == 0:
            return ''
        fields = ''
        for name in self.extended_data.iterkeys():
            fields += SCHEMA_FIELD % {
                                      'name': name,
                                      'type': 'string',
                                      'caption': name
                                     }
        return SCHEMA % {'fields': fields}

    def format_extended_data(self):
        if len(self.extended_data) == 0:
            return ''
        arrays = ''
        for name, values in self.extended_data.iteritems():
            formated_values = '\n'.join([EXTENDED_DATA_VALUE % str(v) for v in values])
            arrays += EXTENDED_DATA_ARRAY % {
                                             'name': name,
                                             'values': formated_values
                                            }
        return EXTENDED_DATA % {'arrays': arrays}

    def __str__(self):
        return TRACK % {
                        'name': self.name,
                        'altitudeMode': self.altitude_mode,
                        'times': self.format_times(),
                        'coords': self.format_coords(),
                        'schema': self.format_schema(),
                        'extendedData': self.format_extended_data()
                       }

