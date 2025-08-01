# vacants

This is a web app to track vacant properties. It imports data from the City of Oklahoma City's [abandoned buildings list](https://www.okc.gov/departments/development-services/code-enforcement/abandoned-buildings). Additionally, we use neighborhood boundaries from the City of OKC's [open data site](https://data.okc.gov/).

The backend is built on Django, connected to a Postgres/PostGIS database. Since the buildings list is published as a PDF, PyPDF2 is used to parse it.

The frontend uses Bootstrap for responsive layout, Leaflet for map, and jQuery/jQuery UI.

## How to install on Heroku
*(tested July 2025)*
* Create your project/app on Heroku.
* Set environment variables:
    * SECRET_KEY
        * Secret key that you will need to generate.
    * MAPBOX_KEY
        * API key for Mapbox.com API. Necessary to get coordinates for addresses.
* You will also need to add the Heroku Geo Buildpack from https://github.com/heroku/heroku-geo-buildpack.git
* Also add the official Python buildpack.
* You will need to create a Postgres database. Go to the "Resources" tabs, and under "Add-on Services" search for "Heroku Postgres". Smallest tier should be sufficient.
* Connect the git repo (under the "Deploy" tab), and deploy.
* Run command "python manage.py migrate" to migrate databases.
* Let's import data now. Run command "python manage.py import_pdf --filename misc_files/AbandonedSep2024.pdf" to read the vacant properties PDF from the City of OKC, and parse it.
* Run command "python manage.py get_geocode" to get geocoding/coordinates for the addresses we have in the table.
* Run command "python manage.py get_neighborhoods" to import neighborhood boundary polygons from shapefiles (included in the project).
* Run command "python manage.py get_city_boundaries" to import city boundary polygons from shapefiles (included in the project).
* **You should be ready to go!**

## How to install on Docker

These instructions may not be complete or may be a work in progress.

* To build in Docker: `docker build -t vacants .`
* To run: `docker run -it --rm -p 8000:8000 vacants`

All of the necessary pip and apt packages should be installed when you build the image.

When you run, you will need to run the `manage.py` commands from the Heroku instructions above.

Note that to run `get_geocode` management command, you will need to set `MAPBOX_KEY` environment var. To do this, run using: `docker run -it --rm -p 8000:8000 -e MAPBOX_KEY=(API KEY HERE) vacants`
