from distutils.core import setup 
from math import atan2
import requests
import xml.etree.ElementTree as ET
import pygrib
#import matplotlib.pyplot as plt
import json
import math
#import pytz
from time import sleep
import sys,os,shutil
import tkinter as tk
from datetime import datetime,timezone, timedelta


setup(windows=["main.py"],
  data_files = [],
  options={"py2exe":{"includes":["pygrib"],'dist_dir': "dist"}})