#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Copyright (C) 2021 by YOUR NAME HERE
#
#    This file is part of RoboComp
#
#    RoboComp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RoboComp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
#

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication
from genericworker import *
from darknet.darknet import *
import numpy as np
import cv2


# If RoboComp was compiled with Python bindings you can use InnerModel in Python
sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel

class SpecificWorker(GenericWorker):
    def __init__(self, proxy_map, startup_check=False):
        super(SpecificWorker, self).__init__(proxy_map)
        self.Period = 2000
        self.network = None
        self.class_names = None
        self.colors = None
        if startup_check:
            self.startup_check()
        else:
            self.timer.timeout.connect(self.compute)
            self.timer.start(self.Period)

    def __del__(self):
        print('SpecificWorker destructor')

    def setParams(self, params):
        #try:
        #	self.innermodel = InnerModel(params["InnerModelPath"])
        #except:
        #	traceback.print_exc()
        #	print("Error reading config params")
        return True


    @QtCore.Slot()
    def compute(self):
        print('SpecificWorker.compute...')
        data = self.camerasimple_proxy.getImage()
        arr = np.fromstring(data.image, np.uint8)
        frame = np.reshape(arr, (data.height, data.width, data.depth))
        cv2.imwrite("frame.jpg", frame)
        if self.network == None:
            self.network, self.class_names, self.colors = load_network("darknet/cfg/yolov4.cfg","darknet/cfg/coco.data","darknet/yolov4.weights")
        img = load_image("frame.jpg".encode("ascii"), 0, 0)
        detections = detect_image(self.network,self.class_names,img)
        print_detections(detections)	
        image = cv2.imread("frame.jpg")
        image = draw_boxes(detections, image, self.colors)
        cv2.imshow("frame",image)

        return True

    def startup_check(self):
        QTimer.singleShot(200, QApplication.instance().quit)




    ######################
    # From the RoboCompCameraSimple you can call this methods:
    # self.camerasimple_proxy.getImage(...)

    ######################
    # From the RoboCompCameraSimple you can use this types:
    # RoboCompCameraSimple.TImage

