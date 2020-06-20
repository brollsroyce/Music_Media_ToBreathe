import serial
import keyboard
import numpy as np
import pandas
import time
import datetime as dt
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import sys

# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = 'COM5'
# be sure to set this to the same rate used on the input device
SERIAL_RATE = 9600

ser = serial.Serial(SERIAL_PORT, SERIAL_RATE, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)	# initialize the serial port which has data incoming
list_of_packets = []

start_reading = input("When data is incoming, press 'q' for 1 sec when you want to stop incoming data. \nPress 's' followed by the Return key to start reading data: ")
if start_reading =='s':
	i = 0
	df = pandas.DataFrame(columns = ["Time(s)", "Abdominal_value", "Chest_value"])
	only_once = 0
	abdominal = 0
	chest = 0
	while ser.is_open:

		if keyboard.is_pressed('q'):
			ser.close()
			print("Data streaming stopped.")
			break

		theBest_time_abd_ch_list = []														# Will eventually have a list of the timestamp, abdominal value and chest value for each incoming packet

		reading = ser.read()															# Read incoming serial data

		in_hex = hex(int.from_bytes(reading, byteorder='little'))								# It is desirable to decode the incoming data as hex values

###### The input packet stream is as follows: start_bit(0x12)	header_bit(0x49)	payload(at least 7 values)	packet_count(increments with new packets)	stop_bit(0x13)			

		if in_hex == hex(18):															# the hex form of 18 is 0x12 which is the start bit of the sequence
			incoming_data_packet = []													# Hence, we initialize the data packet here

		if in_hex != hex(19):															# the hex form of 19 is 0x13 which is the stop bit of the sequence
			incoming_data_packet.append(in_hex)											# Append it to the packet

		if in_hex == hex(19) and len(incoming_data_packet) < 11:								# There are a total of at least 11 values in one packet
			incoming_data_packet.append(in_hex)

		if in_hex == hex(19) and len(incoming_data_packet) > 10:								# This means that it is the end of the packet
			list_of_packets.append(incoming_data_packet)										# Since the packet is complete, append it to a list of complete packets
			print("Packet number: ", i)
			df_length = len(df)			

####################### Here we convert the incoming values into an integer value##############

			high_byte_abd_str = list_of_packets[i][2]
			high_byte_abd_int = int(high_byte_abd_str, 16)
			high_byte_abd_hex = hex(high_byte_abd_int)[2:]

			low_byte_abd_str = list_of_packets[i][3]			
			low_byte_abd_int = int(low_byte_abd_str, 16)
			low_byte_abd_hex = hex(low_byte_abd_int)[2:]

			concatenated_abd = high_byte_abd_hex+low_byte_abd_hex
			int_abdomen = int(concatenated_abd, 16)

			# print("Abdomen (concatenated hex): ", concatenated_abd)
			# print("Abdomen (int): ", int_abdomen)

			high_byte_ch_str = list_of_packets[i][4]
			high_byte_ch_int = int(high_byte_ch_str, 16)
			high_byte_ch_hex = hex(high_byte_ch_int)[2:]

			low_byte_ch_str = list_of_packets[i][5]
			low_byte_ch_int = int(low_byte_ch_str, 16)
			low_byte_ch_hex = hex(low_byte_ch_int)[2:]

			concatenated_ch = high_byte_ch_hex+low_byte_ch_hex
			int_chest = int((high_byte_ch_hex+low_byte_ch_hex),16)

###############################################################################################

			if (int_chest < 30000) or (int_abdomen < 30000) or (int_abdomen > 46000) or (int_chest > 45000):	# This is done because sometimes there are some stray packets with wrong values, noted to be below 30000
				i = i + 1
				continue

			time_s_ms = 0.001 * (int(round(time.perf_counter() * 1000)))								# Time taken for each incoming packet, incremental, called in each iteration

			theBest_time_abd_ch_list = [time_s_ms, int_abdomen, int_chest]

			if only_once==0:
				df.loc[df_length] = theBest_time_abd_ch_list
			elif only_once	==1:
				df.loc[df_length] = theBest_time_abd_ch_list

			print(df)
			df.to_csv(sys.argv[1])
			# print(list_of_packets)
			i = i + 1
			