#!/bin/sh

# $Id$
#
# Run this script to secure your WordPress installation.

echo "$0" | grep -qv sh && exec chmod -R g-w /usr/share/wordpress/wp-content
exec chmod -R g-w ./wp-content
