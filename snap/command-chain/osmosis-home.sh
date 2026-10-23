#!/bin/sh
# osmosis enumerates $HOME/.openstreetmap/osmosis/plugins and aborts when that
# directory is absent. Dot directories in the real home are hidden by the home
# interface, so point the JVM at a writable location instead.
osmosis_home="${SNAP_USER_COMMON:-$HOME}"
mkdir -p "$osmosis_home/.openstreetmap/osmosis/plugins"
export JAVACMD_OPTIONS="-Duser.home=$osmosis_home"

exec "$@"
