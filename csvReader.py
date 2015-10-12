import csv
import sys

#Calculate round trip time based on TCP handshakes

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

		# if you see SYN, this is the beginning of the TCP handshake
		if "[SYN]" in info and "Retransmission" not in info:
			#Save the port number
			port = infoArray[0]

			# store a mapping of IP : array of port numbers
			if dest not in dictionary:
				dictionary[dest] = []

			# map IP to ports
			dictionary[dest].append(port)
			# map port to send time
			portDictionary[port] = [time]

		# if you see SYN, ACK this is the response to the handshake
		elif "[SYN, ACK]" in info and "Retransmission" not in info:
			if "[TCP Out-Of-Order]" in info:
				pass
			else:
				port = infoArray[2]

			# save all the ports for a given IP
			portArray = dictionary[source]
			portArray.append(port)

			# map IP to array of ports
			dictionary[source] = portArray

			# map port to receive time
			portDictionary[port].append(time)

		else:
			pass

	output = open('output.txt','w')
	output.write('Israel Hill\n' + 'EECS 325\n\n')

	# iterate over dictionaries to calcualte avg RTT times
	for serverIp, port in dictionary.iteritems():
				totalRTT = 0
				count = 0
				for p in port:
					timeArray = portDictionary[p]
					# subtract receive time from send time to get trip time
					currentRTT = float(timeArray[1]) - float(timeArray[0])
					count = count + 1
					# add trip time to total time for this IP
					totalRTT = totalRTT + currentRTT

				# calcualte avg RTT time
				avgRTT = totalRTT/count
				output.write("Server IP: " + serverIp + '\n')
				output.write("Average RTT: " + str(avgRTT) + '\n\n')

finally:
	f.close()
	output.close()
