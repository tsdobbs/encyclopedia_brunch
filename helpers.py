#helpers.py - Short functions that are used more than once elsewhere but are too long to write out more than once

import datetime
import markdown
import requests, json

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

#Takes a list of posts and translates the 'notes' field in each post from Markdown to HTML
def translate_markdown_notes(posts):
	count = 0
	fail_list = list()
	for post in posts:
		post.html_notes = markdown.markdown(post.notes)
		if post.html_notes != post.notes and post.html_notes != "<p>" + post.notes + "</p>":
			count +=1
			fail_list.append(post.title)
	return count, fail_list

#replaces special characters with their URL encoding so that urls don't get all weird
def url_cleaner(url):
	url = url.replace('&','%26')
	return url

#For submitting new episodes
#Takes the title of an episode and searches Wikipedia for a list of images on the closest related page
#Removes any images that are too small (<800x600) from the list, then returns a best guess and a few other options
#If it can't find a page on Wikipedia or there are no good images, returns an empty list
def get_image_selection(title):
	scaled_image_list = list()

	api_url = 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=images&titles=' + title + '&imlimit=max&redirects'
	raw_image_json = requests.get(api_url).text
	raw_image_dict = json.loads(raw_image_json)
	returned_pages = raw_image_dict['query']['pages'].keys()
	raw_image_list = list()
	for page in returned_pages:
		try:
			for image in raw_image_dict['query']['pages'][page]['images']:
				if '.svg' not in image['title']: raw_image_list.append(url_cleaner(image['title']))
		except KeyError:
			pass

	if raw_image_list:
		#get size of all the listed images
		api_url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=imageinfo&titles=" + "|".join(raw_image_list) + "&iiprop=size"
		image_size_json = requests.get(api_url).text
		image_size_dict = json.loads(image_size_json)
		returned_pages = image_size_dict['query']['pages'].keys()
		big_image_list = list()
		for page in returned_pages:
			width = int(image_size_dict['query']['pages'][page]['imageinfo'][0]['width'])
			height = int(image_size_dict['query']['pages'][page]['imageinfo'][0]['height'])
			if width > 800 and height > width/2.5 and height < width * 1.5: big_image_list.append(url_cleaner(image_size_dict['query']['pages'][page]['title']))

		if big_image_list:
			#of the images that meet size restrictions, takes the first 5, then requests urls of the thumbnails of those images at 1000px wide
			#if the image is <1000px wide naturally, Wikimedia helpfully returns the original image instead of a scaled one
			api_url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=imageinfo&titles=" + "|".join(big_image_list[:10]) + "&iiprop=url&iiurlwidth=1000"
			scaled_image_json = requests.get(api_url).text
			scaled_image_dict = json.loads(scaled_image_json)
			returned_pages = scaled_image_dict['query']['pages'].keys()
			for page in returned_pages:
				scaled_image_list.append(scaled_image_dict['query']['pages'][page]['imageinfo'][0]['thumburl'])

	return scaled_image_list