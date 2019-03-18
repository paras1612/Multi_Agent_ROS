#!/usr/bin/env python

import linecache

f_obj1 = open("/home/mandeep/Desktop/swarm_sitl2.plan","r")

f_obj2 = open("/home/mandeep/Desktop/swarm_sitl2.txt","w")

for i in range(45,274,19):
	data1 = linecache.getline('/home/mandeep/Desktop/swarm_sitl2.plan',i).rstrip().lstrip()
	data2 = linecache.getline('/home/mandeep/Desktop/swarm_sitl2.plan',i+1).lstrip()

	data3 = data1+data2
	data3.rstrip(',,')
	#print data[0] 
	f_obj2.write(str(data3))
	#f_obj2.write(str(data2))


f_obj1.close()
f_obj2.close()
