"""
    useyourfeelings

    2014.09.29 raidercodebear@gmail.com 
"""

import os
from app import create_app

useyourfeelings = create_app(os.getenv('UYF_CONFIG') or 'default')
