#!/usr/bin/python

import time
import random
import os

# Config
# -
# rows-per-file : How many rows do you want in each file 
# generated by the script
rows = 500000

# tstamp_start: The first file has this timestamp, and 
# successive files have it incrementing by 1 in each file
tstamp_start = 1234567890
tstamp_end = 1234571790
tstamp_step = 15

# out_filename_prefix : This is the prefix. It will always
# be suffixed by '.timestamp'
out_filename_prefix = 'random_timeseries'

# out_filepath: All the files generated are queued in this 
# directory. Make sure it exists
out_filepath = '/root/gitrepo/mysql_monitor/datafiles/'

# max_queued_files: After this many files are generated, 
# the script waits , until somebody starts consuming files.
max_queued_files = 100 # max-files-to-create. Then wait!

# Main
#
while tstamp_start <= tstamp_end: 

	# -- if dir is full , sleep --
	if len(os.listdir(out_filepath))>=max_queued_files:
		time.sleep(1); continue

	# -- generate a random set of uids, values
	values = dict()

	for uid in random.sample(xrange(1000000),rows):
		values[uid]=random.randint(1,100)
	
	# -- create file handle --
	filename = '%s%s.%s' %(out_filepath, out_filename_prefix, tstamp_start)

	tmpfile = filename+'.tmp'
	fh = open(tmpfile, 'w')

	# -- write data and close --
	for uid, value in values.iteritems():
		fh.write('%s,%s,%s\n'%(uid, tstamp_start, value))

	# -- close handle and cleanup --
	fh.close()
	os.rename(tmpfile, filename)
	
	print 'Created file %s' %filename

	# -- increment timestamp
	tstamp_start += tstamp_step
