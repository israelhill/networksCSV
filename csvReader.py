import csv
import sys
import re

f = open(sys.argv[1], 'rt')

try:
	reader = csv.reader(f)
	dictionary = {}
	portDictionary = {}

	for row in reader:
		
		info = row[6]
		source = row[2]
		dest = row[3]
		time = row[1]

		infoArray = info.split(" ")

		if "[SYN]" in info:
			port = infoArray[0]

			if dest not in dictionary:
				dictionary[dest] = []
			
			dictionary[dest].append(port)
			portDictionary[port] = [time]


			# print "[SYN]  Me: " + source + "  " + "Server: " + dest
			# print "Port: " + port
			# print "\n"
		
		elif "[SYN, ACK]" in info:
			port = infoArray[2]

			portArray = dictionary[source]
			portArray.append(port)
			dictionary[source] = portArray

			portDictionary[port].append(time)

			# print "[SYN, ACK]  Server: " + source + "  " + "Me: " + dest
			# print "Port: " + port
			# print "\n"


	for serverIp, port in dictionary.iteritems():
				# print "Server: " + serverIp
				# print port
				# print "\n"

				totalRTT = 0
				count = 0
				for p in port:
					timeArray = portDictionary[p]
					currentRTT = float(timeArray[1]) - float(timeArray[0])
					count = count + 1
					totalRTT = totalRTT + currentRTT

				avgRTT = totalRTT/count
				print "Server IP: " + serverIp
				print "Average RTT: " + str(avgRTT)
				print "\n"

	#print "__________________________________"

	# for port, times in portDictionary.iteritems():
	# 	print "Port: " + port
	# 	print times
	# 	print "\n"

finally:
	f.close()
