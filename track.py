#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 12:58:25 2021

@author: jacob
"""



import os
import cv2 
import numpy as np


class Track:
    def __init__(self, options):
        self.opt = options
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        
        # kernel for image dilation
        self.kernel = np.ones((2,2),np.uint8)

        # font style
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.Window_name_track = 'Tracked'
        self.Window_name_untrack = 'Preprocessed'
        self.Res_scale = 10
        self.Res_dim = np.multiply([self.opt.sensor_width, self.opt.sensor_height], self.Res_scale)        
        
        
        
    def run(self):        
        self.cap = cv2.VideoCapture(self.opt.movie_name+'.mp4')
        # Read until video is completed
        while(self.cap.isOpened()):
            # Capture frame-by-frame
            ret, img = self.cap.read()
            if (ret == False):
                break
            else:
                fgmask = self.fgbg.apply(img)
            
                # image thresholding
                ret, thresh = cv2.threshold(fgmask, 128, 255, cv2.THRESH_BINARY)
                
                # image dilation
                erosion = cv2.erode(fgmask,self.kernel,iterations = 1)
                dilated = cv2.dilate(erosion,self.kernel,iterations = 1)
                
                # find contours
                contours, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
                
                # shortlist contours appearing in the detection zone
                valid_cntrs = []
                Origs = []
                
                dmy = fgmask.copy()
                for cntr in contours:
                    x,y,w,h = cv2.boundingRect(cntr)
                    if  (cv2.contourArea(cntr) >= 4):
                        #print(cv2.contourArea(cntr))
                        #if (cv2.contourArea(cntr) < 40):
                        #    break
                        valid_cntrs.append(cntr)
                        Origs.append([int(x+h/2), int(y+w/2)])
                        # add contours to original frames
                
                cv2.drawContours(dmy, valid_cntrs, -1, (127,200,0), 2)
                            
                res_cont = cv2.resize(dmy, (self.Res_dim[0], self.Res_dim[1]), interpolation = cv2.INTER_AREA)
                res_mask = cv2.resize(fgmask.copy(), (self.Res_dim[0], self.Res_dim[1]), interpolation = cv2.INTER_AREA)
                res_raw = cv2.resize(img, (self.Res_dim[0], self.Res_dim[1]), interpolation = cv2.INTER_AREA)
                res_cont = cv2.applyColorMap(res_cont, cv2.COLORMAP_HOT)
                res_mask = cv2.applyColorMap(res_mask, cv2.COLORMAP_HOT)
                res_raw = cv2.applyColorMap(res_raw, cv2.COLORMAP_HOT)
                for i in range(len(Origs)):
                    res_cont = cv2.putText(res_cont, 'x:' +str(Origs[i][0]) + ' y:' +str(Origs[i][1]), (Origs[i][0]*self.Res_scale, Origs[i][1]*self.Res_scale), self.font, 0.5, (200, 200, 0), 1)
                
                #cv2.putText(dmy, "vehicles detected: " + str(len(valid_cntrs)), (1, 15), font, 0.3, (0, 180, 0), 1)
                #cv2.line(dmy, (0, 80),(256,80),(100, 255, 255))
                #cv2.imwrite(pathIn+str(i)+'.png',dmy)
                
                #cv2.imshow(self.Window_name_untrack, res_mask)
                #cv2.imshow('raw',res_raw)
                
                Verti = np.concatenate((res_cont, res_raw), axis=0) 
                cv2.imshow(self.Window_name_track, Verti)
            
                cv2.waitKey(90)

     


# cap = cv2.VideoCapture(opts.movie_name+'.mp4')
# # Read until video is completed
# while(cap.isOpened()):
#     # Capture frame-by-frame
#     ret, img = cap.read()
#     fgmask =fgbg.apply(img)

#     # image thresholding
#     ret, thresh = cv2.threshold(fgmask, 128, 255, cv2.THRESH_BINARY)
    
#     # image dilation
#     dilated = cv2.dilate(fgmask,kernel,iterations = 1)
    
#     # find contours
#     contours, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    
#     # shortlist contours appearing in the detection zone
#     valid_cntrs = []
#     Origs = []
    
#     dmy = fgmask.copy()
#     for cntr in contours:
#         x,y,w,h = cv2.boundingRect(cntr)
#         if  (cv2.contourArea(cntr) >= 4):
#             print(cv2.contourArea(cntr))
#             #if (cv2.contourArea(cntr) < 40):
#             #    break
#             valid_cntrs.append(cntr)
#             Origs.append([int(x+h/2), int(y+w/2)])
#             # add contours to original frames
    
#     cv2.drawContours(dmy, valid_cntrs, -1, (127,200,0), 2)
                
#     res_cont = cv2.resize(dmy, (Res_dim[0], Res_dim[1]), interpolation = cv2.INTER_AREA)
#     res_mask = cv2.resize(fgmask.copy(), (Res_dim[0], Res_dim[1]), interpolation = cv2.INTER_AREA)
#     res_raw = cv2.resize(img, (Res_dim[0], Res_dim[1]), interpolation = cv2.INTER_AREA)
#     heatmap = cv2.applyColorMap(res_cont, cv2.COLORMAP_HOT)
#     for i in range(len(Origs)):
#         res_cont = cv2.putText(heatmap, 'x:' +str(Origs[i][0]) + ' y:' +str(Origs[i][1]), (Origs[i][0]*Res_scale, Origs[i][1]*Res_scale), font, 0.5, (200, 200, 0), 1)
    
#     #cv2.putText(dmy, "vehicles detected: " + str(len(valid_cntrs)), (1, 15), font, 0.3, (0, 180, 0), 1)
#     #cv2.line(dmy, (0, 80),(256,80),(100, 255, 255))
#     #cv2.imwrite(pathIn+str(i)+'.png',dmy)
#     cv2.imshow(Window_name_track, heatmap)
#     cv2.imshow(Window_name_untrack, res_mask)
#     cv2.imshow('raw',res_raw)

#     cv2.waitKey(50)






































