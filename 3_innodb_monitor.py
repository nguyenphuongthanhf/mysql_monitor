#!/usr/bin/python

\import time
import random
import os
import re

# Config
# -
# log_file: This is the innodb_log_file that keeps track of
# -statistics. This script parses this file and writes csv.
# It actually does a realtime monitor. Make sure that you create
# -a table called innodb_monitor in your database. That command
# -triggers the creation of the log_file by MySQL
log_file = '/var/log/mysql/error.log'

# out_file: The file to write parsed-stats to
out_file = '/root/gitrepo/mysql_monitor/innodb_monitor_out'

# REMEMBER to turn on innodb_monitoring before starting this 
# - script. To do so, just create a table called innodb_monitor.
# It can be in any database, and contain any columns. Its just 
# - a way to instruct mysql to start logging monitor data .

# Functions
#
def follow(thefile):
    thefile.seek(0,2)      

    while True:
        line = thefile.readline()
        if not line: time.sleep(0.1); continue
        else: yield line

# Main
#
start_time = 0

l_fh = open(log_file, 'r')
o_fh = open(out_file, 'a')

o_fh.write("start_time, pending_log, pending_pool, io_reads, io_writes, io_fsyncs, log_io_per_sec, free_buffers, buff_reads, buff_creates, buff_writes, row_inserts, row_updates, row_reads\n")


while 1:

    for line in follow(l_fh):

	if 'END OF INNODB MONITOR OUTPUT' in line:
		try: 
			o_fh.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" %(start_time, 
					pending_log, pending_pool, io_reads, 
					io_writes, io_fsyncs, log_io_per_sec, free_buffers, 
					buff_reads, buff_creates, buff_writes, row_inserts, 
					row_updates, row_reads))
			o_fh.flush()

		except:pass
		start_time=0

	if start_time:

		if 'Pending flushes' in line:
			excerpt = re.match(r'.*log:(.*);.*pool:(.*)',line)
			pending_log, pending_pool = excerpt.group(1), excerpt.group(2)

		if 'fsyncs/s' in line:
			excerpt = re.match(r'(.*)\sreads.*,.*,\s(.*)\swrites.*,\s(.*)\sfsync',line)
			io_reads, io_writes, io_fsyncs = excerpt.group(1), excerpt.group(2), excerpt.group(3)

		if 'log i/o\'s/second' in line:
			excerpt = re.match(r'.*done,\s(.*)\slog',line)
			log_io_per_sec = excerpt.group(1)

		if 'Free buffers' in line:
			excerpt = re.match(r'Free buffers\s+(.*)',line)
			free_buffers = excerpt.group(1)

		if 'creates/s' in line:
			excerpt = re.match(r'(.*)\sreads.*,\s(.*)\screates.*,\s(.*)\swrites',line)
			buff_reads, buff_creates, buff_writes = excerpt.group(1), excerpt.group(2), excerpt.group(3)

		if 'deletes' in line:
			excerpt = re.match(r'(.*)\sinsert.*,\s(.*)\supdate.*,.*,\s(.*)\sread',line)
			row_inserts, row_updates, row_reads = excerpt.group(1), excerpt.group(2), excerpt.group(3)

	try: start_time = re.match(r'\d+\s(.*)\sINNO',line).group(1)
	except : continue
