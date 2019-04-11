# mavros
main commands, control scripts, swarm packages and other essentials.
Open issues freely of any kind!
To start new work, check [Tasks.md](https://github.com/paras1612/mavros/blob/master/Tasks.md) file

# Requirements
- Linux (Ubuntu 16.04 recommended)
- [ROS](http://www.ros.org/install/)
- [MAVROS](http://ardupilot.org/dev/docs/ros-install.html#installing-mavros)
- [SITL(Software In The Loop)](http://ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html)
- Ground Control Stations
  - [QGroundControl](qgroundcontrol.com) (Recommended) 
  - Mission Planner (On windows)
  
# How to start?
- Make a new ros workspace or use our ardupilot_ws preferabely in same folder where SITL is installed. 
- Move to the directory, Remake the directory using `catkin_make`
- source the workspace using `source ./devel/setup.bash`.
- Now move to the directory containing script named demo-swarm.py
- Open the file, change the path variable according to your file directory structure, save the file
- Run `python demo-swarm.py`
- Enter the number of vehicles, you want to spawn
- It'll open the terminals for each instantiated vehicle with a seperate SYS_THISMAV id, which you'll be able to cross check
- Then, a ros script will be started, which will connect all the vehicles (This may fail)
- Open a new terminal, run `rqt`, go to the menu either on menu bar or window's title bar, choose Plugins > Robot Tools > Runtime Monitor
- Check if there is any error or warning
- If not, you're done with successfully initiating all the vehicles
- Go to your GCS, and connect to the respected UDP port of the vehicle, which you can find by writing `output` on the respective SITL terminal. You'll see every vehicle on the same window.
