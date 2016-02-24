# encyclopedia_brunch
The website for the Encyclopedia Brunch podcast

Thanks for looking at this repository! This is the backend code for encyclopediabrunch.com.
It was written from scratch (and with the help of a lot of tutorials) by Tim Dobbs.

=======================================================================================

To run:
This code runs on the Flask microframework. Install this before running - http://flask.pocoo.org/
It also uses the SQLAlchemy extension for Flask - http://flask-sqlalchemy.pocoo.org/2.1/
It also also uses the Flask-WTF for forms - https://flask-wtf.readthedocs.org/en/latest/

=======================================================================================

Javascript requirements:
To make the media player work, include the standard mediaelement.js files in static/js/mediaelement - http://mediaelementjs.com/
To make responsive design work, include bootstrap.js and bootstrap.min.js in static/js - http://getbootstrap.com/2.3.2/
Finally, to make the pagination widget at the bottom of the posts work, include jquery.hoverIntent.js in static/js - http://cherne.net/brian/resources/jquery.hoverIntent.html

=======================================================================================

Content NOT included:
When looking for shows to display, the code looks for a SQLite database called 'eb.db', which is not included in this repository. Details of the model for this database can be found in models.py
Images are stored in static/img, but most image locations are not hardcoded, so it will depend what location you enter into eb.db
