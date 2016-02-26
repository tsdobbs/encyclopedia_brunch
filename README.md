# encyclopedia_brunch
The website for the Encyclopedia Brunch podcast

Thanks for looking at this repository! This is the backend code for http://encyclopediabrunch.com.
It was written from scratch (and with the help of a lot of tutorials) by Tim Dobbs.  

=======================================================================================

###Files:
* run.py - Run this file to start the Flask server
* \__init\__.py - Initializes the Flask framework and the SQLAlchemy extension
* config.py - Configures SQLAlechmy to open the correct database from which to read content
* models.py - Defines the database models for the app
* views.py - Maps URLs to appropriate controllers, runs the backend code, and returns information to the appropriate view templates
* helpers.py - Short helper functions, used mostly in views.py
* templates
  * layout.html - The main layout for the website. All other HTML views extend off of this one
  * home.html - The default load page for the site
  * posts.html - Displays all shows, paginated. Also used to display individual shows
  * about.html - The 'About The Show' page
  * submit.html - Not functional. Will contain form to allow creators to submit new episodes inside web interface
  * rss.xml - Generates the RSS feed when it is requested
  * 404.html
* static
  * css - Folder containing .css files
* examplesfromk
  * unit test examples - not currently applicable to this project, but will be adjusted if we decide to use unit tests here.

======================================================================================

###To run:  
This code runs on the Flask microframework. Install before running - http://flask.pocoo.org/  
It also uses the SQLAlchemy extension for Flask - http://flask-sqlalchemy.pocoo.org/2.1/  
It also also uses the Flask-WTF for forms - https://flask-wtf.readthedocs.org/en/latest/  
**Once these prerequisites are met, run run.py from the command line to start the Flask server**

=======================================================================================

###Javascript requirements:  
To make the media player work, include the standard mediaelement.js files in static/js/mediaelement - http://mediaelementjs.com/  
To make responsive design work, include bootstrap.js and bootstrap.min.js in static/js - http://getbootstrap.com/2.3.2/  
Finally, to make the pagination widget at the bottom of the posts work, include jquery.hoverIntent.js in static/js - http://cherne.net/brian/resources/jquery.hoverIntent.html  

=======================================================================================

###Content NOT included:  
When looking for shows to display, the code looks for a SQLite database called 'eb.db', which is not included in this repository.   Details of the model for this database can be found in models.py  
Images should be stored in static/img/[filename]. Post image locations are not hardcoded, but rather stored in the post column in eb.db
