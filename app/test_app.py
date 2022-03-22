from urllib import response
import pytest
from app import *
from flask import current_app


def test_help():
    assert isinstance(help(), str)


def test_all_positions():
    pass
    # with app.app_context():
    #     current_app.config["ENV"]
    #     r = all_positions()
    #     print(r)
        

def test_epoch_position():
    # epoch name
    pass

def test_all_sightings():
    pass

def test_all_sightings_countries():
    pass

def test_sighting_specific_country():
    # country 
    pass

def test_sighting_region():
    # region 
    pass

def test_sighting_all_cities():
    # region country 
    pass

def test_sighting_city():
    # city 
    pass


test_all_positions()
