import pytest
import sys
sys.path.append("/home/chuan/software/gnss")
from utils.time_converter import *


def test_isCommonYear():
    
    assert(True==isLeapYear(2008))
    assert(False==isLeapYear(2009))

def test_gpst2utc():
    gps_week = 0
    gps_seconds = 0
    assert(datetime(1980,1,6,0,0,0)==gpst2utc(0, 0))
    assert(datetime(1980,1,6,0,0,1) == gpst2utc(0, 1))
    assert(datetime(1980,1,23,0,0,0) == gpst2utc(2, 259200))


if __name__ == "__main__":
    test_gpst2utc()