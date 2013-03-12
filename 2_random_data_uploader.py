#!/usr/bin/python
import time
import random
import os
import MySQLdb
import sys


# Config
# -
# src_filepath: The location of source_files to be uploaded.
# This should be set to the same directory, that the random
# -data_generator writes to.
src_filepath = '/root/gitrepo/mysql_monitor/datafiles/'

# disregard_pattern: Internal usage. The random_data_generator
# -generates files suffixed with '.tmp' and then issues a 'mv'
# -to rename them without the suffix. We dont want to consume
# -the files before they are completely generated
disregard_pattern = '.tmp'

# mysql-settings: destination hostname, dbname and tblname 
# -that all the files should be uploaded to
server = 'localhost'
db = 'perftest'
tbl = 'part_no_idx_yes_signed_no'
username = 'root'
pwd = ''


# Functions
#
def sorted_ls(path):
	mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
	return list(sorted(os.listdir(path), key=mtime))

# Main
#

# -- connect to db --	
try:
	conn = MySQLdb.connect(host=server, user=username, passwd=pwd,
			       db=db, local_infile=1)
except:
	print 'Cannot connect to db'
	sys.exit()
else:
	print 'Connected to db..'
	curs = conn.cursor()

# -- upload files --
while True:
	files = sorted_ls(src_filepath)

	if len(files) == 0: 
		time.sleep(1)
		continue

	for file in files:

		if disregard_pattern in file: continue

		# -- upload the file --
		sql = 'LOAD DATA LOCAL INFILE "%s%s" INTO TABLE %s FIELDS '
		sql += 'TERMINATED BY "," LINES TERMINATED BY "\\n" (uid, tstamp, value)'

		sql = sql%(src_filepath, file, tbl)
	
		start = time.time()
		curs.execute(sql)
		conn.commit()

		humantime = time.strftime("%H:%M:%S", time.localtime())
		print '%s,%s\n' %(humantime, int(time.time() - start))

		os.remove("%s%s" %(src_filepath, file))
