# vehicleDetection

This component allows the user to detect Vehicle in the camera feed in real time. It uses [Darknet YOLO v4](https://github.com/alexeyab/darknet#requirements) in the backend to identify the objects and predict the bounding box. Currently the model is trained on MS COCO dataset and can identify 80 object categories. For object categories please refer to this [link](https://github.com/AlexeyAB/darknet/blob/master/data/coco.names). the model will be trained to identify the following objects : Lane - pedestrian - vehicle  - traffic light  - fire hydrant  - stop sign.


## Resolving dependencies

This section assumes the user has already installed the RoboComp core library and pulled Robolab's components according to this [README guide](https://github.com/robocomp/robocomp).

For dependencies, please ensure that the dependencies are satisfied as mentioned on the github of [Darknet YOLO v4](https://github.com/alexeyab/darknet#requirements).

Next download the Darknet Yolo v4 from the [following link](https://drive.google.com/file/d/1DGXKlEHD8cpGqYi-5dtErt_r8tNPH18-/view?usp=sharing). Use this model only to avoid debugging and resolving path issues. Place the zip file in the folder `vehicleDetection/` and extract there.

After dependencies are installed build the Darknet Yolo model using following commands:

```
cd ~/robocomp/components/vehicleDetection/darknet
make
```

Refer to the Makefile for the build specifications if required.
## Configuration parameters
As any other component, *vehicleDetection* needs a configuration file to start. In
```
etc/config
```
you can find an example of a configuration file. We can find there the following lines:
```
# Proxies for required interfaces
CameraSimpleProxy = camerasimple:tcp -h localhost -p 10005

# This property is used by the clients to connect to IceStorm.
TopicManager.Proxy=IceStorm/TopicManager:default -p 9999

Ice.Warn.Connections=0
Ice.Trace.Network=0
Ice.Trace.Protocol=0
```

## Starting the component
To avoid changing the *config* file in the repository, we can copy it to the component's home directory, so changes will remain untouched by future git pulls:

```
cd ~/robocomp/components/vehicleDetection
```
```
cp etc/config etc/config-run
```

After editing the new config file, build the component by:

```
cmake .
make
```

Now in order to run the component, follow these below steps. Ensure that the model is build and weights downloaded and placed in the correct folder as mentioned above.

Open one more terminal.

Terminal 1:
```
cd hardware/camera/camerasimple
python src/camerasimple.py etc/config-run
```

Terminal 2:
```
cd cd ~/robocomp/components/vehicleDetection
python src/vehicleDetection.py 
```

Once the component is running, user can see the camera feed with bounding box across the objects in a pop-up window.