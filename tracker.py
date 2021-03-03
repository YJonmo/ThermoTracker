#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 13:11:35 2021

@author: jacob
"""

from track import Track
from options import ThermoOptions
from functions import text2MP4

options = ThermoOptions()
opts = options.parse()


if __name__ == "__main__":
    
    text2MP4(opts.sensor_height, opts.sensor_width, opts.data_path, opts.movie_name, opts.ambient_temp)
    tracker = Track(opts)
    tracker.run()
