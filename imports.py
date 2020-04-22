# Author:  Meryll Dindin
# Date:    11 April 2020
# Project: Funnel

import re
import os
import json
import pytz

from lxml import etree
from datetime import datetime

from flask import Flask
from flask import request
from flask import Response
from flask_cors import CORS