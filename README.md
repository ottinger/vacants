# vacants

This is a web app to track vacant properties. It imports data from the City of Oklahoma City's [abandoned buildings list](https://www.okc.gov/departments/development-services/code-enforcement/abandoned-buildings). Additionally, we use neighborhood boundaries from the City of OKC's [open data site](https://data.okc.gov/).

The backend is built on Django, connected to a Postgres/PostGIS database. Since the buildings list is published as a PDF, PyPDF2 is used to parse it.

The frontend uses Bootstrap for responsive layout, Leaflet for map, and jQuery/jQuery UI.

## How to install on Heroku

* Create your project/app on Heroku.
* Set environment variables:
    * BUILD_WITH_GEO_LIBRARIES=1
    * IS_HEROKU=1
    * SECRET_KEY
        * Secret key that you will need to generate.
    * MAPBOX_KEY
        * API key for Mapbox API. Necessary to get coordinates for addresses.
* Before you try to build this project, you will need to add the Heroku apt buildpack from https://github.com/heroku/heroku-buildpack-apt. This is required to install the GDAL library (gdal-bin) necessary to work with geospatial data. The library name is specified in Aptfile, and Heroku will automatically install it if you have the apt buildpack.
* Also add the official Python buildpack.
* Add the git repo, and deploy.
* Now it's time to set up the database. Install the Heroku Postgres addon.
* Run command "python manage.py migrate" to migrate databases.
* Let's import data now. Run command "python manage.py import_pdf" to get the vacant properties PDF from the City of OKC, and parse it.
* Run command "python manage.py get_geocode" to get geocoding/coordinates for the addresses we have in the table.
* Run command "python manage.py get_neighborhoods" to import neighborhood boundary polygons from shapefiles (included in the project).