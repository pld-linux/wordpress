#!/bin/sh

# $Id$
#
# Run this script to let your WordPress web-interface modify some files
# (plugins and themes). Do not forget to run secure.sh when you'll finish.

echo "$0" | grep -qv sh && exec chmod -R g+w /usr/share/wordpress/wp-content
exec chmod -R g+w ./wp-content
