import pytest
from app import *


load_data_into_file()
def return_instructions():
    assert isinstance(return_instructions(),str)==True

def test_return_epoch():
    assert isinstance(return_epoch(),str)==True

def test_return_specific_epoc():
    assert isinstance(return_specific_epoch('2022-057T11:48:56.869Z'),dict)!=True

def test_return_all_countries():
    assert isinstance(return_all_countries(),str)==True

def test_return_specific_country():
    assert isinstance(return_specific_country('Belgium'),dict)!=True

def test_return_regions():
    assert isinstance(return_regions('Belgium'),str)==True

def test_return_a_region():
    assert isinstance(return_a_region('Belgium', 'None'),dict)!=True
def test_return_cities():
    assert isinstance(return_cities('Belgium','None'),str)==True
def test_return_a_city():
    assert isinstance(return_a_city('Belgium','None','Wervik'),dict)!=True


