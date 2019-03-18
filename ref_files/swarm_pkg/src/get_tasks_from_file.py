#!/usr/bin/env python

import linecache

task_list = []
for i in range(1,22):
	data = linecache.getline('/home/mandeep/Desktop/tmp.txt',i)
	data_list = data.split(',')
	data_list[1] = data_list[1].rstrip()
	print data_list
	task_list.append(data_list)

print task_list		