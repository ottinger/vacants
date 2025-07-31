# vacants

**NOTE:** Update is in progress.

This is a web app to track vacant properties. It imports data from the City of Oklahoma City's [abandoned buildings list](https://www.okc.gov/departments/development-services/code-enforcement/abandoned-buildings). Additionally, we use neighborhood boundaries from the City of OKC's [open data site](https://data.okc.gov/).

The backend is built on Django, connected to a Postgres/PostGIS database. Since the buildings list is published as a PDF, PyPDF2 is used to parse it.

The frontend uses Bootstrap for responsive layout, Leaflet for map, and jQuery/jQuery UI.

## How to install on Heroku

* Create your project/app on Heroku.
* Set environment variables:
    * SECRET_KEY
        * Secret key that you will need to generate.
    * MAPBOX_KEY
        * API key for Mapbox.com API. Necessary to get coordinates for addresses.
* You will also need to add the Heroku Geo Buildpack from https://github.com/heroku/heroku-geo-buildpack.git
* Also add the official Python buildpack.
* Add the git repo, and deploy.
* Now it's time to set up the database. Install the Heroku Postgres addon.
* Run command "python manage.py migrate" to migrate databases.
* Let's import data now. Run command "python manage.py import_pdf --filename misc_files/AbandonedSep2024.pdf" to read the vacant properties PDF from the City of OKC, and parse it.
* Run command "python manage.py get_geocode" to get geocoding/coordinates for the addresses we have in the table.
* Run command "python manage.py get_neighborhoods" to import neighborhood boundary polygons from shapefiles (included in the project).
* Run command "python manage.py get_city_boundaries" to import city boundary polygons from shapefiles (included in the project).
* **You should be ready to go!**

## How to install on Docker

Instructions may not be complete or may be work in progress.

* To build in Docker: `docker build -t vacants .`

* To run: `docker run -it --rm -p 8000:8000 vacants`

* If you need to use the get_geocode management command: `docker run -it --rm -p 8000:8000 -e MAPBOX_KEY=(API KEY HERE) vacants`
