from flask import Flask, request
import flask
import requests
import json
import xmltodict
import logging
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

STORE_EXTRA_DATA = False

iss_position_data = {}
iss_sighting_data = {}

@app.route('/help', methods=['GET'])
def help():
    help_string = '''
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
    
    '''
    return help_string

@app.route('/load_data', methods=['GET', 'POST'])
def load_data():
    '''
    Loads in data for all of the epochs from the ISS.

    Args:
        None

    Returns:
        (str): POST or GET message
    '''
    if request.method == 'POST':

        global iss_position_data
        global iss_sighting_data

        iss_position_data.clear()
        iss_sighting_data.clear()

        logging.debug(f'Current directory and contents: {os.listdir()}')
        with open('data/ISS.OEM_J2K_EPH.xml', 'r') as f:
            iss_position_data = xmltodict.parse(f.read())

        with open('data/XMLsightingData_citiesUSA06.xml', 'r') as f:
            iss_sighting_data = json.loads(json.dumps(xmltodict.parse(f.read())))

        return f'Data has been read from file\n'

    else:
        return """
    This is a route for resetting stored data. You must perform
    a POST request to this route to get it to work, e.g.:

    curl -X POST localhost:5011/load_data

"""


@app.route('/position/all', methods=['GET'])
def all_positions():
    '''
    Returns all of the positional data for all of the epochs from the ISS.

    Args:
        None

    Returns:
        all_epochs (flask return object): The positional data for all of the epochs from the ISS.
    '''
    # Getting data
    logging.info('\n\n ***********entering data collection route\n')
    d = get_positional_data()
    logging.debug('data recieved')
    all_epochs = d['ndm']['oem']['body']['segment']['data']['stateVector']

    return flask.jsonify(all_epochs)


@app.route('/position/<epoch_name>', methods=['GET'])
def epoch_position(epoch_name):
    # getting data
    logging.info('\n\n ***********entering data collection route\n')
    d = get_positional_data()
    logging.debug('data recieved')

    # getting specific epoch
    all_epochs = d['ndm']['oem']['body']['segment']['data']['stateVector']
    specific_epoch = [epoch for epoch in all_epochs if epoch["EPOCH"] == epoch_name]
    logging.debug(f'epoch retrieved : \n\n{specific_epoch}')

    return flask.jsonify(specific_epoch)


@app.route('/sightings/all', methods=['GET'])
def all_sightings():
    '''
    Returns all of the sighting data from the USA06 data.

    Args:
        None

    Returns:
        all_sightings (flask return object): The sighting data from USA06
    '''
    # Getting data
    logging.info('entering data collection route\n')
    d = get_sighting_data()
    logging.debug('data recieved')
    all_sightings = d['visible_passes']['visible_pass']
    return flask.jsonify(all_sightings)


@app.route('/sightings/countries', methods=['GET'])
def all_sighting_countries():
    '''
    Returns all of the countries from the USA06 data.

    Args:
        None

    Returns:
        all_sightings (flask return object)(list): list of countries
    '''
    # Getting data
    logging.info('entering data collection route\n')
    d = get_sighting_data()
    logging.debug('data recieved')
    all_sightings = d['visible_passes']['visible_pass']
    countries = []
    for sighting in all_sightings:
        if sighting['country'] not in countries:
            countries.append(sighting['country'])
    return flask.jsonify(countries)


@app.route('/sightings/countries/<country>', methods=['GET'])
def sighting_specific_country(country):
    '''
    Returns all data from a specific country from the USA06 data.

    Args:
        None

    Returns:
        data (flask return object): all data from a specific country from the USA06 data.
    '''
    # Getting data
    logging.info('entering data collection route\n')
    d = get_sighting_data()
    logging.debug('data recieved')
    data = d['visible_passes']['visible_pass']
    logging.debug(f'length of data before country filter: {len(data)}')
    data = [sighting for sighting in data if sighting['country'] == country]
    logging.debug(f'length of data after country filter: {len(data)}')

    return flask.jsonify(data)


@app.route('/sightings/countries/<country>/regions', methods=['GET'])
def sighting_all_regions(country):
    '''
    Returns all regions from a specific country from the USA06 data.

    Args:
        Country (str): country for which the regions will be extracted from.

    Returns:
        data (flask return object)(list): all regions from a specific country from the USA06 data.
    '''
    # Getting data
    d = get_sighting_data()
    data = d['visible_passes']['visible_pass']
    data = [sighting for sighting in data if sighting['country'] == country]
    regions = []
    for sighting in data:
        if sighting['region'] not in regions:
            regions.append(sighting['region'])

    return flask.jsonify(regions)


@app.route('/sightings/regions/<region>', methods=['GET'])
def sighting_region(region):
    '''
    Returns all data for a specific region from the USA06 data.

    Args:
        region (str): region to be searched for.

    Returns:
        region_data (flask return object)(list): all data from a specific region from the USA06 data.
    '''
    # Getting data
    logging.info('entering data collection route\n')
    d = get_sighting_data()
    logging.debug('data recieved')
    data = d['visible_passes']['visible_pass']

    # get only specific region
    logging.debug(f'length of data before region filter: {len(data)}')
    data = [sighting for sighting in data if sighting['region'] == region]
    logging.debug(f'length of data after region filter: {len(data)}')

    return flask.jsonify(data)


@app.route('/sightings/countries/<country>/<region>/cities', methods=['GET'])
def sighting_all_cities(country, region):
    '''
    Returns all cities from a specific country and region from the USA06 data.

    Args:
        country (str): country for data
        region (str): region for data

    Returns:
        cities (flask return object)(list): filtered cities from the USA06 data.
    '''
    # Getting data
    logging.info('entering data collection route\n')
    d = get_sighting_data()
    logging.debug('data recieved')
    data = d['visible_passes']['visible_pass']

    # filtering data
    logging.debug(f'length of data before filter: {len(data)}')
    data = [sighting for sighting in data if (sighting['country'] == country and sighting['region'] == region)]
    logging.debug(f'length of data after filter: {len(data)}')

    # Getting cities
    cities = []
    for sighting in data:
        if sighting['city'] not in cities:
            cities.append(sighting['city'])

    return flask.jsonify(cities)


@app.route('/sightings/cities/<city>', methods=['GET'])
def sighting_city(city):
    '''
    Returns all data for a specific city from the USA06 data.

    Args:
        city (str): city to be searched for

    Returns:
        city_data (flask return object)(list): all data from a specific city from the USA06 data.
    '''
    # Getting data
    logging.info('entering data collection route\n')
    d = get_sighting_data()
    logging.debug('data recieved')
    data = d['visible_passes']['visible_pass']

    # get only specific city
    logging.debug(f'city provided: {city}')
    logging.debug(f'length of data before filter: {len(data)}')
    data = [sighting for sighting in data if sighting['city'] == city]
    logging.debug(f'length of data after filter: {len(data)}')

    # Storing data if in debug mode
    # if logging.root.level == logging.DEBUG:
    #     logging.debug('city sighting data is now stored in "sightings_city.json"')
    #     with open("sightings_city.json", "w") as outfile:
    #         json.dump(data, outfile)

    return flask.jsonify(data)


def get_positional_data():
    '''
    Gets the positional data of the ISS from the nasa public data website.

    Args:
        None
    
    Returns:
        data (dict): posistional data of the ISS in dictionary form
    '''
    
    global iss_position_data
    if len(iss_position_data) == 0:
        logging.error('Data has not yet been loaded in, run the POST /load_data route first')

    return iss_position_data


def get_sighting_data():
    '''
    Gets the sighting data of the ISS from the nasa public data website.

    Args:
        None
    
    Returns:
        data (dict): sighting data of the ISS in dictionary form
    '''
    global iss_sighting_data
    if len(iss_sighting_data) == 0:
        logging.error('Data has not yet been loaded in, run the POST /load_data route first')

    return iss_sighting_data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

