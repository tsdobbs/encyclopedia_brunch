import datetime

def format_date_rss(my_date):
	date_string = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}[my_date.weekday()] + ', '
	date_string += str(my_date.day) + ' '
	date_string += {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}[my_date.month] + ' '
	date_string += str(my_date.year) + ' '
	date_string += my_date.isoformat()[11:19] + ' +0000'
	return date_string