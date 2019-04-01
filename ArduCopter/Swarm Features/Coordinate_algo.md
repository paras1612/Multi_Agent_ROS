<imp> everything is normalised wrt wp1
We add the coordinates of wp1 to generated waypoints


Eqn of a plane using wp1, wp2, wp3
>> cross-product( (wp1-wp2) X (wp3 - wp2) ) get A, B, C
>> Eqn of plane = Ax + By + Cz = 0
Transformation Matrix such that Plane to standard
Transformation inverse take standard to plane

wp1*, wp2*, wp3* = represented in basis of plane(wp1, wp2, wp3)
l1 = wp1*-wp2*
l2 = wp3*-wp2*
K = ratio(path travelled, angle turn)
K = (math.pi - theta)*r/theta => R = k*theta/(math.pi - theta)
L = acute angle bisector of L1 and L2
c = centre of a circle lying on l, such that radii of circle = R and L1 and L2 are tangent to it
looking from +z towards origin
cw direction = l1 x l2 > 0
ccw direction = l1 x l2 < 0

turn_angle = sin-1(l1 X l2)/||l1|| ||l2||
wp*.x such that x belongs to 1,2....(turn_angle/number_of_parts)
wp*.i = ith semi-waypoint
alpha = turn_angle/number_of_parts

wp1*_x - c_x = Rsin(theta)
theta = sin-1((wp1*_x - c_x)/R)
wp*.i_x = c_x + Rcos(theta + i*alpha)
wp*.i_y = c_y + RSin(theta + i*alpha)


convert wp*.i in wp.i by premultiplying by transformation matrix

Done after arriving at wp.i+1 from wp.i

turn after every waypoint by an angle angle between (wp.i+2 - wp.i+1) and current heading