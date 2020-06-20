# This code gives you maximum, minimum, average, +average, -average for chest and abdominal breathing.
# Also, the recorded values of the breathing, which involves max chest breathing, max abdominal breathing and normal breathing are visualized graphically.

# IMPORTS
import csv
import pandas
import matplotlib.pyplot as plt
from matplotlib import style
import sys
import os
import statistics as st
import sys
#import numpy as np

## INITIALIZATIONS

style.use('ggplot')
font = {'family': 'serif',              # Font for graph titles
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }

font1 = {'family': 'serif',              # Font for axes labels
                'color':  'darkblue',
                'weight': 'normal',
                'size': 12,
                }


## READ .CSV DATA
from_csv = pandas.read_csv(sys.argv[1], header = None)
from_csv.drop(0, inplace=True)
from_csv.astype(float)
print("fllaagggg")
print(from_csv)
print("flaggggg")

########################## Convert values from csv file from str to float, then make lists of each #########
float_abd_col = []
float_ch_col = []
float_time_col = []
for floater in range(1, len(from_csv[2]), 1):
	pre_float_abd = (float(from_csv[2][floater]))
	float_abd_col.append(pre_float_abd)

	pre_float_ch = (float(from_csv[3][floater]))
	float_ch_col.append(pre_float_ch)

	pre_float_time = round(float(from_csv[1][floater]),3)
	float_time_col.append(pre_float_time)
# print(float_abd_col)
# print(float_ch_col)
# print(float_time_col)
############################################################################################################

abd_col = float_abd_col[20:]
ch_col = float_ch_col[20:]

################ Creating new values that are easier to work with, a.k.a., normalization##################
new_0_abd = (st.mean(abd_col[1:30]))
new_0_chest = (st.mean(ch_col[1:30]))
# print(new_0_abd)
# print(new_0_chest)

the_abd_list = [round((new_0_abd - x), 3) for x in float_abd_col]	# the list of normalized abdominal values, rounded to 3 decimals
				
# print(the_abd_list)
the_ch_list = [round((new_0_chest - x), 3) for x in float_ch_col]       # the list of normalized chest values, rounded to 3 decimals




for stray in range(2, len(the_abd_list) - 2, 1):
        if abs(the_abd_list[stray-1] - the_abd_list[stray]) > 50:
                the_abd_list[stray] = 0.5*(the_abd_list[stray-1] + the_abd_list[stray+2])

        if abs(the_ch_list[stray-1] - the_ch_list[stray]) > 50:
                the_ch_list[stray] = 0.5*(the_ch_list[stray-1] + the_ch_list[stray+2])


# print(the_ch_list)
#########################################################################################################

################################## Creating the graphs##############################
plt.title('ABDOMINAL BELT VALUES', fontdict = font)
abd_graph = the_abd_list[30:]
timer = float_time_col[30:]
plt.plot(timer, abd_graph, 'g', linewidth = 2)

plt.ylabel('Breath value', fontdict = font1)
plt.xlabel('Time(s)', fontdict = font1)
plt.savefig(sys.argv[3])
plt.show()

plt.title('CHEST BELT VALUES', fontdict = font)
chest_graph = the_ch_list[30:]
plt.plot(timer, chest_graph, 'r', linewidth = 2)

plt.ylabel('Breath value', fontdict = font1)
plt.xlabel('Time(s)', fontdict = font1)
plt.savefig(sys.argv[4])
plt.show()

plt.title('BOTH TOGETHER', fontdict = font)
plt.plot(timer, abd_graph, 'g', linewidth = 2, label = 'Abdominal belt value')
plt.plot(timer, chest_graph, 'r', linewidth = 2, label = 'Chest belt value')
plt.ylabel('Breath value', fontdict = font1)
plt.xlabel('Time(s)', fontdict = font1)
plt.legend()
plt.grid(True, color = 'k')
plt.savefig(sys.argv[5])
plt.show()
####################################################################################
# FIND SPECIFIC VALUES like min max mean etc.
values = open(sys.argv[2], 'w')
max_in_chest = max(the_ch_list)
print("Maximum inhale chest: ", max_in_chest, file = values)
max_in_abd = max(the_abd_list)
print("Maximum inhale abdomen: ", max_in_abd, file = values)
max_out_chest = min(the_ch_list)
print("Maximum exhale chest: ", max_out_chest, file = values)
max_out_abd = min(the_abd_list)
print("Maximum exhale abdomen: ", max_out_abd, file = values)
ovrall_mean_ch = round(st.mean(the_ch_list),3)
print("Mean Chest value:", ovrall_mean_ch, file = values)
ovrall_mean_abd = round(st.mean(the_abd_list),3)
print("Mean Abdomen value:", ovrall_mean_abd, file = values)

