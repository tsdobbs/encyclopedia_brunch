#helpers.py - Short functions that are used more than once elsewhere but are too long to write out more than once

import datetime

#Takes a Python datetime object as input and outputs a string in the preferred format used in RSS feeds.
#[Day of Week], [Day] [Month] [Year] [HH:MM:SS] +[Time Zone]
#Note that this page always publishes in UTC
def format_date_rss(my_date):
	date_string = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}[my_date.weekday()] + ', '
	date_string += str(my_date.day) + ' '
	date_string += {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}[my_date.month] + ' '
	date_string += str(my_date.year) + ' '
	date_string += my_date.isoformat()[11:19] + ' +0000'
	return date_string