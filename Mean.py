# Script Name: Mean.py
# Author : Dimeji Fayomi
# Created : 25 August 2015
# Last Modified :
# Version : 1.0
# Code to sync a specific directory from one mail box to another.

#!/usr/bin/env python

import math

def mean_number(number_list):
   # get the size of the number list
   length = len(number_list)
   sum = 0
   # get the sum of the elements in the list
   for i in range(0, length):
      sum += number_list[i]
   mean_value = sum/length
   return(mean_value)
   

def mode_number(number_list):
   length = len(number_list)   
   top_mode = 0
   top_freq = 0 
   dict_mode = {}
   modes = {}
   for i in range(0, length):
      # Check if number has already been added to dict
      # If added, pass, else get count and add to dict
      if number_list[i] in dict_mode:
         pass
      else:
         dict_mode[number_list[i]] = number_list.count(number_list[i])
         
    # Now find the largest  value in the dict
   top_mode = max(dict_mode, key=dict_mode.get)
   top_freq = dict_mode[top_mode]
    
    # check if there are other numbers with the same frequency
   for mode, freq in dict_mode.iteritems():
      if freq == top_freq:
         # create a new dict and key and value to it
         modes[mode] = freq
      else:
         pass
    
    # check if modes is empty, then return top_mode and top_freq else return modes
   if len(modes) != 0:
      return(modes)
   else:
      return(top_mode)
    
   
def median_number(number_list):
   length = len(number_list)
   sortedlist = sorted(number_list)
   median_position = (length + 1)/2
   index = median_position - 1
   median = sortedlist[index]
   return median
   
# define a list
numlist = []
number = -9
while number != 0:
   print "Enter a number or press 0 to stop entering numbers"
   number = int(raw_input("Enter:"))
   if len(numlist) == 0 and number == 0:
      print "You have not entered any number before  exiting, Enter some numbers!!!"
      number = int(raw_input("Enter:"))
      numlist.append(number)
      continue 
   else:
      if number == 0:
         pass
      else:
         numlist.append(number)
   

print "Mean value is %s" % mean_number(numlist)

#print "Mode  is %s" % mode_number(numlist)
mode_values = mode_number(numlist)
if type(mode_values) is dict:
   for key in mode_values.iterkeys():
      print "Modea are: %s" % key
else:
   print "Mode is: %s" % mode_values
      
print "Median value is %s" % median_number(numlist)

   
