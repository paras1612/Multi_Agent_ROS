import subprocess
import time
path_to_SITL_ardupilot = '/home/vishalsamal/ardupilot'
path_to_launch_file = '/home/vishalsamal/ardupilot_ws/src/swarming/launch'
path_to_template = '/home/vishalsamal/param_files'
vehicle_count = int(input("Enter the number of Vehicles: "))
first_port_number = 14560
port_number = first_port_number
launch_template = '<launch>'


def generator(id, path_to_template, path = "/home",):
	with open(path + '/param_files/mav_' + str(id) + '.parm', 'w') as paramFile:	
		lines = []
		with open(path_to_template + '/template.parm', 'r') as template:
			line = template.readline()
			while line:
				if line.find("SYSID_THISMAV") >= 0:
					lines.append('SYSID_THISMAV\t ' + str(float(id)) + '00000\n')
				else:
					lines.append(line)
				line = template.readline()
			template.close()
		paramFile.writelines(lines)
		paramFile.close()


#Maximum number of vehicle allowed is 10
for count in range(1, min(vehicle_count + 1, 11)):
	generator(count, path_to_template, '/home/vishalsamal')
	#+ ' -w' + ' --add-param-file ' + ' home/anonymous/Desktop/param_files/mav_' + str(count) + '.parm'
	subprocess.Popen(['gnome-terminal','-e' ,'sim_vehicle.py -v ArduCopter -I ' + str(count) + ' -w' + ' --add-param-file ' + ' /home/vishalsamal/param_files/mav_' + str(count) + '.parm' + ' --console'], cwd=path_to_SITL_ardupilot)
	launch_template += '<group ns="vehicle' + str(count) + '">' + '<arg name="fcu_url" default="udp://localhost:' + str(port_number) + '@"/>' + '<arg name="gcs_url" default="" />' + '<arg name="ID" default="' + str(count) + '" />' + '<arg name="tgt_component" default="1" />' + '<arg name="fcu_protocol" default="v2.0" />' + '<include file="$(find mavros)/launch/px4.launch">' + '<arg name="fcu_url" value="$(arg fcu_url)"/>' + '<arg name="gcs_url" value=""/>' + '<arg name="tgt_system" value="$(arg ID)"/>' + '<arg name="tgt_component" value="1"/>' + '</include>' + '</group>'
	port_number += 10

launch_template += "\n </launch>"
#print(launch_template)

with open(path_to_launch_file + '/main_launch.launch', 'w') as launch_file:
	launch_file.write(launch_template)
	launch_file.close()
time.sleep(10)
subprocess.Popen(['gnome-terminal', '-e', 'roslaunch main_launch.launch'], cwd=path_to_launch_file)



