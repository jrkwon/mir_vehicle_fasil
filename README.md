# mir_vehicle_fasil

MIR is the Mobile Intelligent Robotics Lab.
The `mir_vehicle` is a platform name and is followed by a model name, `bolt`. 
This repository is for the Bulldog Bolt of Kettering for the AutoDrive Challenge.

## Contributors

* Jaerock Kwon, Ph.D. Associate Professor
* Shobit Sharma, Research Assistant
* Mohamed Fasil Syed, Research Assistant

## Install

The `mir_vehicle` platform uses Gazebo 9. The ROS Kinetic has Gazeo 7 by default. This version must be removed before the installation of Gazebo 9.

### Remove Gazebo 7

Use the following commands.

```
$ sudo apt remove ros-kinetic-gazebo*
$ sudo apt remove libgazebo*
$ sudo apt remove gazebo*
```

Then, update the repositories of packages.
```
$ sudo apt update
```

### Install Gazebo 9

#### Prep for Gazebo 9 Installation

- Setup your computer to accept software from packages.osrfoundation.org.

```
$ sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
```

- Setup keys

```
$ wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
```

#### Install Gazebo 9 and Developer Packages

- First update the debian database:

```
$ sudo apt update
```

- Next install gazebo-9 and the packages for developers

```
$ sudo apt-get install gazebo9
$ sudo apt-get install libgazebo9-dev
```
- Check the installation
```
$ gazebo
```

### Build

- Clone the mir-vehicle

```
$ git clone https://github.com/jrkwon/mir_vehicle_fasil.git
```

- Install the ros-controllers and some additional ros packages.

```
$ sudo apt install ros-kinetic-ros-controllers
$ sudo apt install ros-kinetic-joint-state-controller
$ sudo apt install ros-kinetic-four-wheel-steering-controller 
$ sudo apt install ros-kinetic-controller-manager
$ sudo apt install ros-kinetic-velodyne-pointcloud
```
- Make
```
$ cd mir_vehicle_fasil
$ catkin_make
```

### Running the trained model
To launch the vehicle model in Gazebo
```
$ cd mir_vehicle 
$ roslaunch mir_vehicle_gazebo bulldogbolt_gazebo.launch
```
To control the vehicle using the trained model, open another terminal and execute the below commands.

**NEED TO CHANGE**
```
$ cd ~/mirvehicle/src/mirvehicle/scripts/Fasil_model
$ python MODEL_RUN.py 2018-02-11-23-28-48
```
## Folder Structure

* `mir_vehicle`: ROS nodes will be located.
* `mir_vehicle_description`: vehicle model. It includes `urdf` and `meshes`. There is a single launch file in `launch` folder. `bulldogbolot_state_publisher.launch` will start `rviz` with the config file, `bulldogbolt_state_publisher.rviz`. This is used to verify that the vehicle's urdf model are well made.
  * `bulldogbolt`: A specific vehicle model name. Under this folder, you must define a vehicle's model.
    * `main.urdf.xacro`: The main urdf. This will be called by launch files. This main urdf includes following three xacros.
    * `properties.urdf.xacro`: This defines the properties of the vehicle. You may need to change this to specify a vehicle model's properties.
    * `structure.urdf.xacro`: This defines the vehicle's body and wheels.
    * `sensors.urdf.xacro`: This defines cameras and laser sensors.
* `mir_vehicle_gazebo`: This is for Gazebo simulation.
  * `config/bulldogbolt_control.yaml`: controller defintions.
  * `launch`
    * `bulldogbolt_empty.launch`: Start the Gazebo server with Bulldogbolt model and a basic world. You need to start `gzclient` in a separate terminal if you want to use Gazebo.
    * `bulldogbolt_gazebo.launch`: Start the Gazebo server and client. This will start `rviz` as well to visualize sensor data. You can use a parameter input for a world name. Use `world:=<world_name>` where the world name can be found at `world` folder. The default world name is `skidpan`. 
    * `bulldogbolt_neighborhood.launch`: This is same as `bulldogbolot_gazebo.launch world:=neighborhood`
    * `mir_vehicle.launch`: This is a generic launch file that will be included by other launch files. There is no need to use this launch file directly.

  * `models`: 3D object models for Gazebo.
  * `worlds`: World files for Gazebo.

## Acknowledgements

This project was possible with the works of Arizona University's the CAT Vehicle Testbed and Dataspeed Inc's ADAS system (dbw_mkz).
