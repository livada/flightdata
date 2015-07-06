import os


AddOption('--prefix',
          dest='prefix',
          nargs=1, type='string',
          action='store',
          metavar='DIR',
          help='installation prefix')
env = Environment(PREFIX = GetOption('prefix'))

# Installation paths
idir_prefix  = '$PREFIX'
idir_bin     = '$PREFIX/bin'
idir_pyshare = '$PREFIX/share/pyshared/flightdata'
Export('env idir_prefix idir_bin idir_pyshare')

env.InstallAs(os.path.join(idir_bin, 'flight2kml'), env.Entry('#bin/flight2kml'))

py_files = Glob('./pyshared/flightdata/*.py',strings=True)
for pyfile in py_files:
    env.InstallAs(os.path.join(idir_pyshare, os.path.split(pyfile)[-1:][0]), pyfile)

env.Alias('install', idir_prefix)


env.Command("uninstall", None, Delete(FindInstalledFiles()))


