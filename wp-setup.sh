#!/bin/sh

# $Id$
#
# Run this script to let your WordPress web-interface modify some files
# (plugins and themes). Do not forget to run secure.sh when you'll finish.

exec chmod -R g+w ./wp-content
