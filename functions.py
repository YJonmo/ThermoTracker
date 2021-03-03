#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 12:39:55 2021

@author: jacob

"""


import numpy as np 
import cv2


"This function reads the raw txt file and converts it to video after "
"preprocessing spets such as background subtraction, nan removal, and minimum temperature threshoulding."
def text2MP4(height, width, data_path, movie_name, ambient_temp):
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    VideoRL = cv2.VideoWriter(movie_name+'.mp4', fourcc, 20, (width, height), 0)
    
    Mag = 10
    #Frame = np.zeros((height,width), np.float32)
    print(data_path)
    Frames= np.loadtxt(data_path, skiprows=2)
    Frames = Frames[:, 0: height*width]
    Frames = Frames.reshape(Frames.shape[0], height, width)
    Frame  = np.zeros((height, width), np.float32)
    
    for frame_ind in range(Frames.shape[0]):
        Frame = Frames[frame_ind,:,:]
        frame_mean = np.nanmean(Frame, axis=0)
        indexes = np.where(np.isnan(Frame)) 
        Frame[indexes] = np.take(frame_mean, indexes[1])
        Frames[frame_ind] = Frame
        
        VideoRL.write(((Frame-ambient_temp)*Mag).astype('uint8'))
        
        
    VideoRL.release()