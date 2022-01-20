import os

import requests

import example
import tracer


def another_logic():
    """Test library call"""
    res = requests.get("http://www.baidu.com", timeout=5)
    return


def TestLogic(x, y):
    another_logic()
    example.do_something(x, y)
    return y


def init_some(number):
    k = 0
    if number > 0:
        k = number
    return k


if __name__ == "__main__":
    Tracer = tracer.Tracer("./")
    tracer.set_tracer(Tracer.tracer)
    example.guess()
    TestLogic(7, 2)
    init_some(1)
    Tracer.tracer_end()
