#!/bin/env python3
from flask import Flask

app = Flask(__name__)

app.route("/")
def home():
    return "Welcome to the flood prediction API.\
        Access the endpoint /api/<int:days>, where days in the number of future days you want to get a prediction for (e.g. /api/23)"
