#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 12:32:50 2021

@author: jacob
"""


import os
import argparse

file_dir = os.path.dirname(__file__)  # the directory that options.py resides in


class ThermoOptions:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Thermal tracker")

        # PATHS
        self.parser.add_argument("--data_path",
                                 type=str,
                                 help="path to the raw data",
                                 default=(file_dir))
        self.parser.add_argument("--log_dir",
                                 type=str,
                                 help="where the video is written to",
                                 default=(file_dir))
        self.parser.add_argument("--movie_name",
                                 type=str,
                                 help="name of the movie to write",
                                 default='movie')
        self.parser.add_argument("--ambient_temp",
                                 type=int,
                                 help="approximate ambient temprature",
                                 default=20)
        self.parser.add_argument("--sensor_height",
                                 type=int,
                                 help="height of thermal sensor",
                                 default=17)
        self.parser.add_argument("--sensor_width",
                                 type=int,
                                 help="width of thermal sensor",
                                 default=35)

    def parse(self):
        self.options = self.parser.parse_args()
        return self.options
