# ISS Position and Sightings App
This repo contains a flask app that obtains and distributes data from the International Space Station. It is a great example of the creation of a flask app that uses ports and contains many modern practices such as docstrings, unit tests, a Dockerfile, and a Makefile.

## Scripts and Folders

#### /data
Contains all of the data used for the app. 

#### app.py
The main flask app. This is where most of the logic of the app happens.

#### Dockerfile
Used to create the docker image.

#### Makefile
Used to assist the building of the containerized app.

#### test_app.py
Tests the functionality of app.py.

## Download the original data
Before running or containerizing the app, it is important to download the orignal data and put it in the /app/data folder. These can be found here:
```
 https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq
```
Under Public Distribution File and XMLsightingData_citiesUSA06

Additionally, these links will work as well and will directly download the data:
```
Public Distribution File:

https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml

XMLsightingData_citiesUSA06:

https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA06.xml
```

## Build a container from the Dockerfile
Once the data is downloaded and is in the folder /data (which is same directory as the Dockerfile), a container can be built from the Dockerfile. To do so, run the command
```
docker build -t rhodgesd/iss_app:latest .
```
Afterwords, to run the app from the container on port 5011, use 
```
docker run -d -p 5011:5000 rhodgesd/iss_app:latest
```
The build and run process of the container is simplified by the Makefile. Instead of running the above commands, you might find it easier to run 
```
make build
make run
or 
make all
```
These will build and run the Docker container.

## Pull an existing container from Dockerhub
Run the command 
```
docker pull rhodgesd/iss_app:latest
```
while having docker installed. You should receive 'latest: Pulling from rhodgesd/iss_app' and then a success message.

## Run the flask app
One can run the flask app by using the following command.
```
flask run -p 5011
```
These commands are convienient as well, and they show any logging that is happening on the server.
```
export FLASK_APP=app.py
export FLASK_ENV=development
```

## How to interact with the app and use all of the routes
Once the app is up and running, you will need to use curl commands to interact and recieve data from the app. The curl commands will look like the following:
```
curl localhost:5011/<route>
```
The route variable will change depending on what information is desired. For all routes and what they do, you can run 'curl localhost:5011/help'. Additionally, here is what the routes do and is the same content provided by the help function:
```
    This app is built to retrieve and filter through ISS position and sighting data.
    Here are all of the routes and what they do:
    ---------------------------------------------------------
    /load_data -> load sighting and positional data into memory
    REQUIRED WHEN FIRST STARTING THE SERVER

    /position/all -> get data from all epochs in the positional data

    /position/<epoch name> -> get data for a specific epoch in the positional data
    EXAMPLE: ../position/2022-042T12:00:00.000Z

    /sightings/all -> get data for all sightings in USA06

    /sightings/countries -> get all countries in sighting data

    /sightings/countries/<country> -> get all sighting data for a particular country
    EXAMPLE: ../sightings/countries/United_States

    /sightings/countries/<country>/regions -> get all regions for a particular country
    EXAMPLE: ../sightings/countries/United_States/regions

    /sightings/regions/<region> -> get all data for a specific region
    EXAMPLE: ../sightings/regions/Massachusetts

    /sightings/countries/<country>/<region>/cities -> get list of cities for a specific country and region
    EXAMPLE: ../sightings/countries/United_States/Massachusetts/cities

    /sightings/cities/<city> -> get all data for a particular city
    EXAMPLE: ../sightings/cities/Flemington
```
### Interpretting the return values of routes
All of the routes return data in some form. For some routes, the data will be a set of strings in a list. This will look like a list of all regions in a particular area, or all cities, etc. There are also routes that return data in the form of a list of dictionaries. In these routes, each data point in the list will contain a lot of information pertaining to a particular sighting or Epoch.

Additionally, there are two data sets which represent different things. All routes with the prefix /positions/... will utilize the positions data set (the Public distribution file) and will give data about each epoch from the ISS. All routes with the prefix /sightings/... will utilize the sighting data set (USA06) and will give information about places on earth where the ISS was observed.

## Citation
NASA is the provider and owner of the data in the data folder. 

NASA (2022). Public Distribution File. Available from: https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml

NASA (2022). XMLsightingData_citiesUSA06. Available from https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA06.xml


