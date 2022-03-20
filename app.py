from flask import Flask
import flask
import requests
import json
import xmltodict
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route('/help', methods=['GET'])
def help():
    help_string = '''
    Here are all of the routes and what they do:

    /position/all -> get data from all epochs in the positional data

    /position/<epoch name> -> get data for a specific epoch in the positional data

    '''
    return help_string


@app.route('/position/all', methods=['GET'])
def all_positions():
    logging.info('\n\n ***********entering data collection route\n')
    d = get_positional_data()
    logging.debug('data recieved')
    all_epochs = d['ndm']['oem']['body']['segment']['data']['stateVector']

    if logging.root.level == logging.DEBUG:
        logging.debug('all positional data is now stored in "positionall.json"')
        with open("positionall.json", "w") as outfile:
            json.dump(all_epochs, outfile)

    return flask.jsonify(all_epochs)


def get_positional_data():
    logging.debug('requesting iss coordinate (positional) data')
    url_data = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    r = requests.get(url=url_data)
    logging.debug('response recieved')
    data = xmltodict.parse(r.content)
    logging.debug('response converted to dictionary')
    logging.debug(f'type of data after parsing: {type(data)}')
    return data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

