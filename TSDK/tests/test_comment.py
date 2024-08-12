from TSDK.api.douyin.h5 import DouyinH5
import pytest

def df(x):
    return x + 1


def test_func():
    assert df(3) == 4

def bb_func():
    assert df(3) == 4