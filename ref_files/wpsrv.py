def waypoint_push_client(data):
    waypoint_clear_client()
    wl = WaypointList()
    wp = Waypoint()
    wp.frame = 3
    wp.command = 22  # takeoff
    wp.is_current = True
    wp.autocontinue = True
    wp.param1 = data[0]['altitude']  # takeoff altitude
    wp.param2 = 0
    wp.param3 = 0
    wp.param4 = 0
    wp.x_lat = data[0]['latitude']
    wp.y_long = data[0]['longitude']
    wp.z_alt = data[0]['altitude']
    wl.waypoints.append(wp)

    for point in data:
        wp = Waypoint()
        wp.frame = 3
        wp.command = 16  # simple point
        wp.is_current = False
        wp.autocontinue = True
        wp.param1 = 0  # takeoff altitude
        wp.param2 = 0
        wp.param3 = 0
        wp.param4 = 0

        wp.x_lat = point['latitude']
        wp.y_long = point['longitude']
        wp.z_alt = point['altitude']
        wl.waypoints.append(wp)
    try:
        service = rospy.ServiceProxy(
            'mavros/mission/push', WaypointPush)
        if service.call(wl.waypoints).success:
            print 'write mission success'
        else:
            print 'write mission error'
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e

def waypoint_clear_client():
        try:
            response = rospy.ServiceProxy(
                'mavros/mission/clear', WaypointClear)
            return response.call().success
        except rospy.ServiceException, e:
            print "Service call failed: %s" % e
            return False