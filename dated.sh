#!/bin/bash
# simple script to create dated dirs
# run this script as root. change paths if you're not using standard.

date=`date +%m%d`
date2=`date --date '1 days ago' +%m%d`  # this is just an example

# the following will make sure people can't upload to old dated dirs
chmod o-w /home/glftpd/site/INCOMING/MP3/*

# this will create a new dated dir
mkdir /home/glftpd/site/INCOMING/MP3/$date
chmod 777 /home/glftpd/site/INCOMING/MP3/$date

# This will create a 'today' link to today's dated directory
cd /home/glftpd/site
rm MP3-today
ln -s ./INCOMING/MP3/$date MP3-today
rm MP3-yesterday
ln -s ./INCOMING/MP3/$date2 MP3-yesterday
